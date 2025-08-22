# store/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from clothingStore.views import CategoryViewSet, ProductViewSet, CartItemViewSet, OrderViewSet
from django.contrib import admin

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
