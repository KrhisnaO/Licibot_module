from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('ingreso/', views.login_view, name='ingreso'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('crear_licitaciones/', views.liccreac, name='crear_licitaciones'),

]

