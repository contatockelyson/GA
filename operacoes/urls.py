from django.urls import path

from . import views

app_name = 'operacoes'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dash/<str:perfil>/', views.dashboard_perfil, name='dashboard_perfil'),
    path('dash/<str:perfil>/modulos/<str:modulo>/', views.lista_modulo, name='lista_modulo_perfil'),
    path('dash/<str:perfil>/modulos/<str:modulo>/exportar/', views.exportar_modulo, name='exportar_modulo_perfil'),
    path('dash/<str:perfil>/modulos/<str:modulo>/novo/', views.criar_registro, name='criar_registro_perfil'),
    path('dash/<str:perfil>/modulos/<str:modulo>/<int:pk>/editar/', views.editar_registro, name='editar_registro_perfil'),
    path('dash/<str:perfil>/modulos/<str:modulo>/<int:pk>/excluir/', views.excluir_registro, name='excluir_registro_perfil'),
    path('modulos/<str:modulo>/', views.lista_modulo, name='lista_modulo'),
    path('modulos/<str:modulo>/exportar/', views.exportar_modulo, name='exportar_modulo'),
    path('modulos/<str:modulo>/novo/', views.criar_registro, name='criar_registro'),
    path('modulos/<str:modulo>/<int:pk>/editar/', views.editar_registro, name='editar_registro'),
    path('modulos/<str:modulo>/<int:pk>/excluir/', views.excluir_registro, name='excluir_registro'),
]
