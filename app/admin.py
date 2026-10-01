from django.contrib import admin
from .models import *


admin.site.register(Ocupacao)
admin.site.register(Cidade)
admin.site.register(Area_do_saber)
admin.site.register(Turno)
admin.site.register(Disciplina)
admin.site.register(Turmas)
admin.site.register(Ocorrencias)
admin.site.register(TipoAvaliacao)

# ================= INLINES =================

class CursoDisciplinaInline(admin.TabularInline):
    model = CursoDisciplina
    extra = 1

class InstituicaoCursosInline(admin.TabularInline):
    model = Curso
    extra = 1


class MatriculasInline(admin.TabularInline):
    model = Matriculas
    extra = 1

class FrequenciaInline(admin.TabularInline):
    model = Frequencia
    extra = 1


class AvaliacaoInline(admin.TabularInline):
    model = Avaliacao
    extra = 1

# ================= ADMINS =================

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'instituicao')
    search_fields = ('nome',)
    inlines = [CursoDisciplinaInline]

@admin.register(Instituicao_de_ensino)
class InstituicaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    inlines = [InstituicaoCursosInline]

@admin.register(Pessoa)
class EstudantesAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'email')
    search_fields = ('nome', 'cpf')
    inlines = [MatriculasInline, FrequenciaInline, AvaliacaoInline]
