from django.db import models
from django.utils import timezone

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    data_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Marca(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    data_inclusao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    codigo_registro = models.CharField(max_length=50, unique=True)
    codigo_barras = models.CharField(max_length=13, unique=True)
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.PROTECT, 
        related_name='produtos'
    )
    marca = models.ForeignKey(
        Marca, 
        on_delete=models.PROTECT, 
        related_name='produtos'
    )
    data_cadastro = models.DateTimeField(auto_now_add=True)
    custo = models.DecimalField(max_digits=10, decimal_places=2)
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2)
    informacoes_adicionais = models.TextField(null=True, blank=True)
    em_promocao = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-data_cadastro']
    
    def __str__(self):
        return self.nome


class Setor(models.Model):
    letra = models.CharField(max_length=1, unique=True)
    descricao = models.CharField(max_length=200, null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'
        ordering = ['letra']
    
    def __str__(self):
        return f"Setor {self.letra}"


class Escaninho(models.Model):
    codigo = models.IntegerField()
    setor = models.ForeignKey(
        Setor, 
        on_delete=models.CASCADE, 
        related_name='escaninhos'
    )
    produto = models.ForeignKey(
        Produto, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='escaninhos'
    )
    quantidade = models.IntegerField(default=0)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Escaninho'
        verbose_name_plural = 'Escaninhos'
        ordering = ['setor', 'codigo']
        unique_together = ['setor', 'codigo']
    
    def __str__(self):
        return f"Escaninho {self.codigo} - {self.setor}"