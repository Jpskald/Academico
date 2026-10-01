"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('pessoas/', PessoasView.as_view(), name='pessoas'),
    path('pessoas/<int:pk>/', PessoaDetalheView.as_view(), name='pessoa_detalhe'),
    path('cursos/', CursosView.as_view(), name='cursos'),
    path('disciplinas/', DisciplinasView.as_view(), name='disciplinas'),
    # PWA Service Worker
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/javascript'), name='sw.js'),
    # APIs para Offline Sync
    path('api/pessoa/criar/', api_criar_pessoa, name='api_criar_pessoa'),
    path('api/curso/criar/', api_criar_curso, name='api_criar_curso'),
    path('api/disciplina/criar/', api_criar_disciplina, name='api_criar_disciplina'),
]
