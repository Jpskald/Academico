from django.db import models

# Create your models here.



class Ocupacao(models.Model):
    nome = models.CharField(max_length = 100, verbose_name="Nome da Ocupação")
    def __str__(self):
        return f"{self.nome}"
    class Meta:
        verbose_name = "Ocupação"
        verbose_name_plural = "Ocupações"

class Cidade(models.Model):
    nome = models.CharField(max_length=100, verbose_name= "Nome da Cidade")
    uf = models.CharField(max_length=100, verbose_name= "Unidade Federativa")
    def __str__(self):
        return f"{self.nome}, {self.uf}"
    class Meta:
        verbose_name="Cidade"
        verbose_name_plural="Cidades"


class Instituicao_de_ensino(models.Model):
    nome = models.CharField(max_length=100, verbose_name = "Nome da Instituição de ensino")
    site = models.CharField(max_length=100, verbose_name = "Site da Instituição")
    email = models.CharField(max_length=100, verbose_name = "Email da Instituição")
    telefone = models.CharField(max_length=100, verbose_name = "Telefone da instituição")
    cidade = models.ForeignKey(Cidade, on_delete = models.CASCADE, verbose_name="Cidade da Instituição")
    def __str__(self):
        return f"{self.nome}, {self.site}"
    class Meta:
        verbose_name = "Instituição de ensino"
        verbose_name_plural = "Instituições de ensino"



class Pessoa(models.Model):
    nome = models.CharField(max_length=100, verbose_name = "Nome")
    nome_do_pai = models.CharField(max_length=100, verbose_name = "Nome do pai")
    nome_da_mae = models.CharField(max_length = 100, verbose_name = "Nome da mae")
    cpf = models.CharField(max_length=20, verbose_name = "CPF")
    data_nasc = models.DateField(verbose_name = "Data de nascimento")
    email = models.CharField(max_length = 100, verbose_name = "Email")
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE, verbose_name = "Nome da Cidade")
    ocupacao = models.ForeignKey(Ocupacao, on_delete=models.CASCADE, verbose_name="Nome da Ocupação")
    def __str__(self):
        return f"{self.nome}, {self.email}, {self.cpf}"
    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"

class Area_do_saber(models.Model):
    nome = models.CharField(max_length=100, verbose_name = "Área do saber")
    def __str__(self):
        return f"{self.nome}"
    class Meta:
        verbose_name = "Área do saber"
        verbose_name_plural = "Áreas do saber"

class Curso(models.Model):
    nome = models.CharField(max_length=100, verbose_name = "Nome do Curso")
    carga_horaria_total =models.CharField(max_length=100, verbose_name = "Carga horária total")
    duracao_meses = models.CharField(max_length=100, verbose_name = "Duração do curso em meses")
    area_saber = models.ForeignKey(Area_do_saber, on_delete=models.CASCADE, verbose_name="Área do saber")
    instituicao = models.ForeignKey(Instituicao_de_ensino, on_delete=models.CASCADE, verbose_name = "Nome da Instituição de Ensino")
    def __str__(self):
        return f"{self.nome}"
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

class Turno(models.Model):
    nome = models.CharField(max_length=100, verbose_name = "Turno")
    def __str__(self):
        return f"{self.nome}"
    class Meta:
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"

class Disciplina(models.Model):
    nome = models.CharField(max_length=100, verbose_name = "Disciplina")
    area_saber = models.ForeignKey(Area_do_saber, on_delete=models.CASCADE, verbose_name="Área do saber")
    def __str__(self):
        return f"{self.nome}"
    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"

class Matriculas(models.Model):
    instituicao = models.ForeignKey(Instituicao_de_ensino, on_delete=models.CASCADE, verbose_name = "Instituição de ensino")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, verbose_name = "Curso")
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, verbose_name = "Nome")
    data_inicio = models.DateField(verbose_name = "Data de início")
    data_previsao_termino = models.DateField(verbose_name = "Previsão de término")
    def __str__(self):
        return f"{self.pessoa}"
    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"

class Frequencia(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, verbose_name = "Curso")
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, verbose_name = "Nome")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, verbose_name = "Disciplina")
    numero_faltas = models.IntegerField(verbose_name = "Número de faltas")
    def __str__(self):
        return f"{self.numero_faltas}"
    class Meta:
        verbose_name = "Frequência"
        verbose_name = "Frequências"

class Turmas(models.Model):
    nome = models.CharField(max_length=100, verbose_name = "Turma")
    turno = models.CharField(max_length=100, verbose_name = "Turno")
    def __str__(self):
        return f"{self.nome}"
    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"

class Ocorrencias(models.Model):
    descricao = models.CharField(max_length=100, verbose_name = "Descrição da ocorrência")
    data = models.DateField(verbose_name = "Data da ocorrência")
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, verbose_name = "Nome")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, verbose_name = "Curso")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, verbose_name = "Disciplina")
    def __str__(self):
        return f"{self.descricao}"
    class Meta:
        verbose_name = "Ocorrencia"
        verbose_name_plural = "Ocorrencias"

class CursoDisciplina(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, verbose_name = "Curso")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, verbose_name = "Disciplina")
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE, verbose_name = "Turno")
    carga_horaria = models.IntegerField(verbose_name="Carga horária")
    def __str__(self):
        return f"{self.disciplina}, {self.curso}"

class TipoAvaliacao(models.Model):
    nome = models.CharField(max_length=100, verbose_name = "Tipo de avaliação")
    def __str__(self):
        return f"{self.nome}"
    class Meta:
        verbose_name = "Tipo de avaliação"
        verbose_name_plural = "Tipos de avaliação"

class Avaliacao(models.Model):
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, verbose_name="Aluno")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, verbose_name="Disciplina")
    tipo = models.ForeignKey(TipoAvaliacao, on_delete=models.CASCADE, verbose_name="Tipo de Avaliação")
    nota = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Nota")
    
    def __str__(self):
        return f"{self.pessoa.nome} - {self.tipo.nome}: {self.nota}"
    
    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"