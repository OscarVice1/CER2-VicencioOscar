from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path("", views.mostrar_eventos, name="mostrar_eventos"),
    path("registro/", views.registrar_usuario, name="registrar_usuario"),
    path("logout/", LogoutView.as_view(next_page="mostrar_eventos"), name="logout"),
    path("inscribir/<int:evento_id>/", views.inscribir_evento, name="inscribir_evento"),
    path("mis-eventos/", views.mis_eventos, name="mis_eventos"),
    path(
        "anular/<int:inscripcion_id>/",
        views.anular_inscripcion,
        name="anular_inscripcion",
    ),
    path(
        "login/",
        LoginView.as_view(template_name="core/iniciar_sesion.html"),
        name="login",
    ),
]
