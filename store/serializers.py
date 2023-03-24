from rest_framework import serializers

from . import models

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Collection
        fields = ['id', 'title', 'product_count']
    
    product_count = serializers.IntegerField()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'title', 'slug', 'inventory', 'unit_price', 'collection']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ['id', 'name', 'description', 'date']
    
    def create(self, validated_data):
        product_id = self.context['product_id']
        return models.Review.objects.create(product_id=product_id, **validated_data)

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'title', 'unit_price']
        
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, cartitem: models.CartItem):
        return cartitem.quantity * cartitem.product.unit_price
    
    class Meta:
        model = models.CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: models.Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
    class Meta:
        model = models.Cart
        fields = ['id', 'items', 'total_price']
