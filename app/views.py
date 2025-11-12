from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import ProtectedError  # ← IMPORTANTE: Adicionar essa linha
from .models import Categoria, Marca, Produto, Setor, Escaninho
from .serializers import (
    CategoriaSerializer, MarcaSerializer, 
    ProdutoSerializer, ProdutoListSerializer,
    SetorSerializer, SetorDetailSerializer,
    EscaninhoSerializer, EscaninhoDetailSerializer
)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        """Tratamento de erro ao deletar categoria com produtos"""
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {
                    'error': 'Não é possível deletar esta categoria pois existem produtos vinculados a ela.',
                    'detail': 'Remova ou reassocie os produtos antes de deletar a categoria.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        """Tratamento de erro ao deletar marca com produtos"""
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {
                    'error': 'Não é possível deletar esta marca pois existem produtos vinculados a ela.',
                    'detail': 'Remova ou reassocie os produtos antes de deletar a marca.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['em_promocao', 'marca', 'categoria']
    ordering_fields = ['data_cadastro', 'valor_venda']
    ordering = ['-data_cadastro']
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProdutoListSerializer
        return ProdutoSerializer
    
    def get_queryset(self):
        queryset = Produto.objects.all()
        
        setor = self.request.query_params.get('setor', None)
        if setor:
            queryset = queryset.filter(escaninhos__setor__letra=setor).distinct()
        
        escaninho = self.request.query_params.get('escaninho', None)
        if escaninho:
            queryset = queryset.filter(escaninhos__codigo=escaninho).distinct()
        
        codigo = self.request.query_params.get('codigo', None)
        if codigo:
            queryset = queryset.filter(codigo_registro__icontains=codigo)
        
        codigo_barras = self.request.query_params.get('codigo_barras', None)
        if codigo_barras:
            queryset = queryset.filter(codigo_barras__icontains=codigo_barras)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def mais_antigos(self, request):
        """Endpoint para retornar os 10 produtos mais antigos"""
        produtos_antigos = Produto.objects.order_by('data_cadastro')[:10]
        serializer = ProdutoListSerializer(produtos_antigos, many=True)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """Verificar permissão para alterar promoção"""
        if 'em_promocao' in request.data:
            if not request.user.is_staff:
                return Response(
                    {'error': 'Apenas administradores podem alterar promoções'},
                    status=status.HTTP_403_FORBIDDEN
                )
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Verificar permissão para alterar promoção (PATCH)"""
        if 'em_promocao' in request.data:
            if not request.user.is_staff:
                return Response(
                    {'error': 'Apenas administradores podem alterar promoções'},
                    status=status.HTTP_403_FORBIDDEN
                )
        return super().partial_update(request, *args, **kwargs)


class SetorViewSet(viewsets.ModelViewSet):
    queryset = Setor.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return SetorDetailSerializer
        return SetorSerializer
    
    def destroy(self, request, *args, **kwargs):
        """Tratamento de erro ao deletar setor com escaninhos"""
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {
                    'error': 'Não é possível deletar este setor pois existem escaninhos vinculados a ele.',
                    'detail': 'Remova os escaninhos antes de deletar o setor.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class EscaninhoViewSet(viewsets.ModelViewSet):
    queryset = Escaninho.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['setor', 'produto']
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return EscaninhoDetailSerializer
        return EscaninhoSerializer