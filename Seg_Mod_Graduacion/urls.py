from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Seg_Mod_Graduacion import views

urlpatterns = [

    path('prueba', views.prueba, name='prueba'),
    
    #segguimiento modalidad de graduacion investigacion cientifica
    path('invcientifica/agregar_investigacion/', views.agregar_investigacion, name='agregar_investigacion'),
    path('proyectos/vista_investigacion/',views.vista_investigacion, name='vista_investigacion'),

] 