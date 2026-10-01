from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.forms import inlineformset_factory
from .models import *
from .forms import PessoaForm, CursoForm, DisciplinaForm
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Definindo os Formsets (equivalente aos inlines do Admin)
MatriculasFormSet = inlineformset_factory(
    Pessoa, Matriculas,
    fields=['curso', 'instituicao', 'data_inicio', 'data_previsao_termino'],
    extra=1, can_delete=True
)
FrequenciaFormSet = inlineformset_factory(
    Pessoa, Frequencia,
    fields=['curso', 'disciplina', 'numero_faltas'],
    extra=1, can_delete=True
)
AvaliacaoFormSet = inlineformset_factory(
    Pessoa, Avaliacao,
    fields=['disciplina', 'tipo', 'nota'],
    extra=1, can_delete=True
)

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

class PessoasView(View):
    def get(self, request):
        pessoas = Pessoa.objects.all()
        form = PessoaForm()
        return render(request, 'pessoas.html', {'pessoas': pessoas, 'form': form})

    def post(self, request):
        form = PessoaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pessoas')
        
        pessoas = Pessoa.objects.all()
        return render(request, 'pessoas.html', {'pessoas': pessoas, 'form': form})

class PessoaDetalheView(View):
    def get(self, request, pk):
        pessoa = get_object_or_404(Pessoa, pk=pk)
        form = PessoaForm(instance=pessoa)
        matriculas_fs = MatriculasFormSet(instance=pessoa)
        frequencia_fs = FrequenciaFormSet(instance=pessoa)
        avaliacao_fs = AvaliacaoFormSet(instance=pessoa)
        return render(request, 'pessoa_detalhe.html', {
            'pessoa': pessoa, 'form': form,
            'matriculas_fs': matriculas_fs,
            'frequencia_fs': frequencia_fs,
            'avaliacao_fs': avaliacao_fs,
        })

    def post(self, request, pk):
        pessoa = get_object_or_404(Pessoa, pk=pk)
        form = PessoaForm(request.POST, instance=pessoa)
        matriculas_fs = MatriculasFormSet(request.POST, instance=pessoa)
        frequencia_fs = FrequenciaFormSet(request.POST, instance=pessoa)
        avaliacao_fs = AvaliacaoFormSet(request.POST, instance=pessoa)

        if form.is_valid() and matriculas_fs.is_valid() and frequencia_fs.is_valid() and avaliacao_fs.is_valid():
            form.save()
            matriculas_fs.save()
            frequencia_fs.save()
            avaliacao_fs.save()
            return redirect('pessoa_detalhe', pk=pk)

        return render(request, 'pessoa_detalhe.html', {
            'pessoa': pessoa, 'form': form,
            'matriculas_fs': matriculas_fs,
            'frequencia_fs': frequencia_fs,
            'avaliacao_fs': avaliacao_fs,
        })

class CursosView(View):
    def get(self, request):
        cursos = Curso.objects.all()
        form = CursoForm()
        return render(request, 'cursos.html', {'cursos': cursos, 'form': form})

    def post(self, request):
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cursos')
        cursos = Curso.objects.all()
        return render(request, 'cursos.html', {'cursos': cursos, 'form': form})

class DisciplinasView(View):
    def get(self, request):
        disciplinas = Disciplina.objects.all()
        form = DisciplinaForm()
        return render(request, 'disciplinas.html', {'disciplinas': disciplinas, 'form': form})

    def post(self, request):
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('disciplinas')
        disciplinas = Disciplina.objects.all()
        return render(request, 'disciplinas.html', {'disciplinas': disciplinas, 'form': form})


# ===== APIS PARA OFFLINE SYNC =====

@csrf_exempt
def api_criar_pessoa(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'invalid method'}, status=405)
    try:
        d = json.loads(request.body)
        Pessoa.objects.create(
            nome=d.get('nome', ''),
            nome_do_pai=d.get('nome_do_pai', ''),
            nome_da_mae=d.get('nome_da_mae', ''),
            cpf=d.get('cpf', ''),
            data_nasc=d.get('data_nasc', '2000-01-01'),
            email=d.get('email', ''),
            cidade_id=d.get('cidade_id'),
            ocupacao_id=d.get('ocupacao_id'),
        )
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
def api_criar_curso(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'invalid method'}, status=405)
    try:
        d = json.loads(request.body)
        Curso.objects.create(
            nome=d.get('nome', ''),
            carga_horaria_total=d.get('carga_horaria_total', ''),
            duracao_meses=d.get('duracao_meses', ''),
            area_saber_id=d.get('area_saber_id'),
            instituicao_id=d.get('instituicao_id'),
        )
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
def api_criar_disciplina(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'invalid method'}, status=405)
    try:
        d = json.loads(request.body)
        Disciplina.objects.create(
            nome=d.get('nome', ''),
            area_saber_id=d.get('area_saber_id'),
        )
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
