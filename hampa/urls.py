from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
from cart.views import *
from accounts.views import ProfileViewSet, AddressViewSet

router = routers.DefaultRouter()
router.register(r'carts', CartViewSet)
router.register(r'cart_items', CartItemViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order_items', OrderItemViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'address', AddressViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('producers/', include('producers.urls')),
    url(r'^', include(router.urls)),
]
