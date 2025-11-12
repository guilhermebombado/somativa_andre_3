from django.contrib import admin
from .models import Categoria, Marca, Produto, Setor, Escaninho


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data_registro']
    search_fields = ['nome']
    list_per_page = 20


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cnpj', 'data_inclusao']
    search_fields = ['nome', 'cnpj']
    list_per_page = 20


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo_registro', 'categoria', 'marca', 'valor_venda', 'em_promocao', 'data_cadastro']
    list_display_links = ['nome', 'codigo_registro']
    search_fields = ['nome', 'codigo_registro', 'codigo_barras']
    list_filter = ['em_promocao', 'categoria', 'marca']
    list_per_page = 20


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ['letra', 'descricao', 'data_cadastro']
    search_fields = ['letra']
    list_per_page = 20


@admin.register(Escaninho)
class EscaninhoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'setor', 'produto', 'quantidade', 'data_cadastro']
    list_display_links = ['codigo']
    search_fields = ['codigo']
    list_filter = ['setor']
    list_per_page = 20