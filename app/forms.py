from django import forms
from .models import Pessoa, Curso, Disciplina

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ['nome', 'nome_do_pai', 'nome_da_mae', 'cpf', 'data_nasc', 'email', 'cidade', 'ocupacao']
        # Adicionando as classes do Bootstrap para ficar bonito igual o resto do site
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'nome_do_pai': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_da_mae': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apenas números'}),
            'data_nasc': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'exemplo@email.com'}),
            'cidade': forms.Select(attrs={'class': 'form-control'}),
            'ocupacao': forms.Select(attrs={'class': 'form-control'}),
        }
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nome', 'carga_horaria_total', 'duracao_meses', 'area_saber', 'instituicao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do curso'}),
            'carga_horaria_total': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Carga horária total'}),
            'duracao_meses': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Duração em meses'}),
            'area_saber': forms.Select(attrs={'class': 'form-control'}),
            'instituicao': forms.Select(attrs={'class': 'form-control'}),
        }
class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome', 'area_saber']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da disciplina'}),
            'area_saber': forms.Select(attrs={'class': 'form-control'}),
        }
