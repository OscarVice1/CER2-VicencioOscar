from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Evento, Asistente
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


def mostrar_eventos(request):

    now = timezone.now()

    evento_proximo_main = (
        Evento.objects.filter(fecha_hora__gte=now).order_by("fecha_hora").first()
    )

    eventos_lista = Evento.objects.filter(fecha_hora__gte=now).order_by("fecha_hora")
    eventos_lista = eventos_lista.exclude(pk=evento_proximo_main.pk)

    contexto = {
        "evento_proximo_main": evento_proximo_main,
        "eventos": eventos_lista,
        "now": now,
    }

    return render(request, "core/index.html", contexto)


def registrar_usuario(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(
                request,
                f"{usuario.username}! Tu cuenta ha sido creada.",
            )
            return redirect("mostrar_eventos")
        else:
            messages.error(request, "Error al registrarse.")

    else:
        form = UserCreationForm()

    contexto = {"form": form}
    return render(request, "core/registro_usuario.html", contexto)


@login_required
def inscribir_evento(request, evento_id):

    evento = get_object_or_404(Evento, id=evento_id)

    if evento.fecha_hora < timezone.now():
        messages.error(
            request, "No puedes inscribirte a un evento que ya ha finalizado."
        )
        return redirect("mostrar_eventos")

    if evento.plazas_disponibles <= 0:
        messages.error(request, "Ya no quedan plazas disponibles.")
        return redirect("mostrar_eventos")

    ya_inscrito = Asistente.objects.filter(usuario=request.user, evento=evento).first()
    if ya_inscrito:
        messages.warning(request, f'Ya estás inscrito en el evento "{evento.titulo}".')
        return redirect("mostrar_eventos")

    evento.plazas_disponibles -= 1
    evento.save()

    Asistente.objects.create(usuario=request.user, evento=evento)

    messages.success(request, f'Te has inscrito correctamente a "{evento.titulo}".')
    return redirect("mostrar_eventos")


@login_required
def mis_eventos(request):
    now = timezone.now()
    inscripciones = (
        Asistente.objects.filter(usuario=request.user)
        .select_related("evento")
        .order_by("evento__fecha_hora")
    )

    contexto = {"inscripciones": inscripciones, "now": now}

    return render(request, "core/mis_eventos.html", contexto)


@login_required
@require_POST
def anular_inscripcion(request, inscripcion_id):

    inscripcion = get_object_or_404(Asistente, id=inscripcion_id)

    if inscripcion.usuario != request.user:
        messages.error(request, "No tienes permiso para anular esta inscripción.")
        return redirect("mis_eventos")

    evento_asociado = inscripcion.evento

    inscripcion.delete()

    evento_asociado.plazas_disponibles += 1
    evento_asociado.save()

    messages.success(
        request,
        f'Has anulado tu inscripción para el evento "{evento_asociado.titulo}".',
    )

    return redirect("mis_eventos")
