from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Repositorio_Titulados import views

urlpatterns = [
    path("listar_titulados/",views.listar_titulados, name="listar_titulados"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)