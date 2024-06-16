from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('ingreso/', views.login_view, name='ingreso'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('mantenedor_preguntas/<action>/<id>/', views.mantenedor_preguntas, name='mantenedor_preguntas'),
    path('administrador/', views.administrador, name='administrador'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('historial_usu/', views.historial_usu, name='historial_usu'),
    path('vendedor/', views.vendedor, name='vendedor'),
    path('gerente/', views.gerente, name='gerente'),
    path('buscar_lici/', views.buscar_lici, name='buscar_lici'),
    path('historial_lici/', views.historial_lici, name='historial_lici'),
    path('subir_archivo/', views.subir_archivo, name='subir_archivo'),
    path('leer_pdf/<str:id>/', views.leer_pdf, name='leer_pdf'),
    path('seleccionar_preguntas/<str:licitacion_id>/', views.seleccionar_preguntas, name='seleccionar_preguntas'),
    path('historial_errores/', views.historial_errores, name='historial_errores'),
]

