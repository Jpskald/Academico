from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Ocupacao)
admin.site.register(Cidade)
admin.site.register(Instituicao_de_ensino)
admin.site.register(Pessoa)
admin.site.register(Area_do_saber)
admin.site.register(Curso)
admin.site.register(Turno)
admin.site.register(Disciplina)
admin.site.register(Matriculas)
admin.site.register(Frequencia)
admin.site.register(Turmas)
admin.site.register(Ocorrencias)

class CursoDisciplinaInline(admin.TabularInline):
    model = CursoDisciplina
    extra = 1

class CursoAdmin(admin.ModelAdmin):
    inlines = [CursoDisciplinaInline]

class OcupacaoPessoasInline(admin.TabularInline):
    model = Ocupacao
    extra = 1

class PessoasAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    inlines = [OcupacaoPessoasInline]

class InstituicaoCursosInline(admin.TabularInline):
    model = Curso
    extra = 1

class InstituicaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    inlines = [InstituicaoCursosInline]

class AreadosaberCursosInline(admin.TabularInline):
    model = Curso
    extra = 1

class AreadoSaberAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    inlines = [AreadosaberCursosInline]

class CursosDisciplinasInline(admin.TabularInline):
    model = Disciplina
    extra = 1

class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    inlines = [CursosDisciplinasInline]

