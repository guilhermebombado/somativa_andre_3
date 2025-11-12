from rest_framework import serializers
from .models import Categoria, Marca, Produto, Setor, Escaninho


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'


class ProdutoSerializer(serializers.ModelSerializer):
    # Serializer para criar/atualizar (recebe IDs)
    class Meta:
        model = Produto
        fields = '__all__'


class ProdutoListSerializer(serializers.ModelSerializer):
    # Serializer para listar (mostra dados completos)
    categoria = CategoriaSerializer(read_only=True)
    marca = MarcaSerializer(read_only=True)
    
    class Meta:
        model = Produto
        fields = '__all__'


class SetorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setor
        fields = '__all__'


class EscaninhoSerializer(serializers.ModelSerializer):
    # Serializer para criar/atualizar
    class Meta:
        model = Escaninho
        fields = '__all__'


class EscaninhoDetailSerializer(serializers.ModelSerializer):
    # Serializer para listar (mostra dados do produto)
    produto = ProdutoListSerializer(read_only=True)
    setor = SetorSerializer(read_only=True)
    
    class Meta:
        model = Escaninho
        fields = '__all__'


class SetorDetailSerializer(serializers.ModelSerializer):
    # Serializer para listar (mostra todos os escaninhos)
    escaninhos = EscaninhoDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Setor
        fields = '__all__'