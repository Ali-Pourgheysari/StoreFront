from django.shortcuts import get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from store.serializers import ProductSerializer
from .models import Product

# Create your views here.
@api_view()
def product_list(request):
    queryset = Product.objects.all()
    serialize = ProductSerializer(queryset, many=True)
    return Response(serialize.data)

@api_view()
def product_detail(request, id):
    product = get_list_or_404(Product, pk=id)[0]
    serializer = ProductSerializer(product)
    return Response(serializer.data)