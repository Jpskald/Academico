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
    area_saber = models.ForeignKey(Area_do_saber, verbose_name="Área do saber")
    instituicao = models.ForeignKey(Instituicao_de_ensino, verbose_name = "Nome da Instituição de Ensino")
    def __str__(self):
        return f"{self.nome}"
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"



