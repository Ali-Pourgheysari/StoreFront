from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, 'products')
router.register('collection', views.CollectionViewSet)
router.register('carts', views.CartViewSet, 'carts')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', views.CartItemsViewSet, basename='cart-items')

# URLConf
urlpatterns = router.urls + products_router.urls + cart_router.urls