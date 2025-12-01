from django.contrib import admin
from .models import Evento, Asistente


class AsistenteInline(admin.TabularInline):
    model = Asistente
    extra = 0
    readonly_fields = ("usuario", "fecha_registro")
    can_delete = False
    verbose_name_plural = "Asistentes Inscritos"

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):

    list_display = (
        "titulo",
        "fecha_hora",
        "lugar",
        "valor",
        "plazas_disponibles",
        "plazas_ocupadas",
    )

    inlines = [AsistenteInline]

    def plazas_ocupadas(self, obj):

        return obj.asistente_set.count()

    plazas_ocupadas.short_description = "Asistentes Inscritos"


@admin.register(Asistente)
class AsistenteAdmin(admin.ModelAdmin):
    list_display = ("usuario", "evento", "fecha_registro")
    list_filter = ("evento", "usuario")
