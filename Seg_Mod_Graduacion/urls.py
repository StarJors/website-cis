from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Seg_Mod_Graduacion import views

urlpatterns = [

    path('prueba', views.prueba, name='prueba'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)