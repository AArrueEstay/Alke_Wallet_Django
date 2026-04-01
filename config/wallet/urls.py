from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_usuarios, name='lista_usuarios'),

    path('dashboard/<int:usuario_id>/', views.dashboard, name='dashboard'),

    path('crear/', views.crear_usuario, name='crear_usuario'),
    path('editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),

    path('transaccion/<int:usuario_id>/', views.crear_transaccion, name='crear_transaccion'),
]