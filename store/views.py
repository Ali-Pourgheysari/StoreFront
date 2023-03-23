
from django.db.models import Count
from django.shortcuts import get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin
from django_filters.rest_framework import DjangoFilterBackend

from store import serializers

from . import models
from . import pagination
from . import filters


# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    pagination_class = pagination.DefaultPagination
    

    def destroy(self, request, *args, **kwargs):
        if models.OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
            return Response({"error": "Product can not be deleted because it associats with orders."})
        return super().destroy(request, *args, **kwargs)

class CollectionViewSet(ModelViewSet):
    queryset = models.Collection.objects.annotate(product_count=Count('products')).all()
    serializer_class = serializers.CollectionSerializer    

    def destroy(self, request, *args, **kwargs):
        if models.Product.objects.filter(collectioin_id = kwargs['pk']).count() > 0:
            return Response({"error": "Collection can not be deleted because it associats with products."})
        return super().destroy(request, *args, **kwargs)
    
class ReviewViewSet(ModelViewSet):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        return models.Review.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    
class CartViewSet(CreateModelMixin, GenericViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer