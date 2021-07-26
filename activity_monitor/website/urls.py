from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cpu_info', views.cpu_info, name='cpu_info'),
    path('memory_info', views.memory_info, name='memory_info'),
    path('disc_info', views.disc_info, name='disc_info'),
    path('ip_info', views.ip_info, name='ip_info'),
]

# desafio, pegar o input do usuário pelo terminal e listar os arquivos da pasta digitada no terminal