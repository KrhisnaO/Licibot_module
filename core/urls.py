from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('ingreso/', views.login_view, name='ingreso'),
    path('recuperar_pass/', views.recuperar_pass, name='recuperar_pass'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('mantenedor_preguntas/<action>/<id>/', views.mantenedor_preguntas, name='mantenedor_preguntas'),
    path('administrador/', views.administrador, name='administrador'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('historial_usu/', views.historial_usu, name='historial_usu'),
    path('editar_usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('desc_user_excel/', views.desc_user_excel, name='desc_user_excel'),
    path('desc_lici_excel/', views.desc_lici_excel, name='desc_lici_excel'),
    path('vendedor/', views.vendedor, name='vendedor'),
    path('gerente/', views.gerente, name='gerente'),
    path('historial_lici/', views.historial_lici, name='historial_lici'),
    path('historial_lici_con_usuario/', views.historial_lici_con_usuario, name='historial_lici_con_usuario'),
    path('subir_archivo_lici/<str:id>/', views.subir_archivo_lici, name='subir_archivo_lici'),
    path('leer_pdf/<str:id>/', views.leer_pdf, name='leer_pdf'),
    path('seleccionar_preguntas/<str:licitacion_id>/', views.seleccionar_preguntas, name='seleccionar_preguntas'),
    path('historial_errores/', views.historial_errores, name='historial_errores'),
    path('validar_licitacion/', views.validar_licitacion, name='validar_licitacion'),
]

