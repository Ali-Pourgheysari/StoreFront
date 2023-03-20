from urllib.request import Request
from django.shortcuts import get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count
from rest_framework.views import APIView
from store import serializers
from . import models


# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

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
    
