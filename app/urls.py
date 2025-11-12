from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet, 
    MarcaViewSet, 
    ProdutoViewSet,
    SetorViewSet, 
    EscaninhoViewSet
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'marcas', MarcaViewSet, basename='marca')
router.register(r'produtos', ProdutoViewSet, basename='produto')
router.register(r'setores', SetorViewSet, basename='setor')
router.register(r'escaninhos', EscaninhoViewSet, basename='escaninho')

urlpatterns = [
    path('', include(router.urls)),
]