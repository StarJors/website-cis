from django.urls import path ,include
from . import views
from django.conf.urls import handler403
#from .views import handle_permission_denied
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('hometrabajos', views.hometrabajos, name='hometrabajos'),
    path('repoin', views.repoin, name='repoin'),
    #proyectos de interacion social
    path('homesocial/proyecto_detail/', views.proyecto_detail, name='proyecto_detail'),
    path('homesocial/clasificar_proyectos/', views.clasificar_proyectos, name='clasificar_proyectos'),
    path('homesocial/global_settings/', views.global_settings_view, name='global_settings'),
    path('homesocial/proyectosin_so/', views.proyectosin_so, name='proyectosin_so'),
]
#handler403 = handle_permission_denied
