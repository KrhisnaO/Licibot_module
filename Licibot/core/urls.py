from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('ingreso/', views.login_view, name='ingreso'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('crear_licitaciones/', views.liccreac, name='crear_licitaciones'),
    path('administrador/', views.administrador, name='administrador'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('historial_usu/', views.historial_usu, name='historial_usu'),
    path('vendedor/', views.vendedor, name='vendedor'),
    path('gerente/', views.gerente, name='gerente'),

]

