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
    path('homesocial/inv_soc_settings/', views.inv_soc_settings, name='inv_soc_settings'),
    path('homesocial/proyectosin_so/', views.proyectosin_so, name='proyectosin_so'),
    
    #####    tareas admin   #####
    path('Tareas/Tipo/listart/', views.listart, name='listart'),
    path('Tareas/Tipo/listart/creart/', views.creart, name='creart'),
    path('Tareas/Tipo/listart/editart/<int:pk>/', views.editart, name='editart'),
    path('Tareas/Tipo/listart/eliminart/<int:pk>/', views.eliminart, name='eliminart'),
]
#handler403 = handle_permission_denied
