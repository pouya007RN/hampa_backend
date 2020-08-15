from django.urls import path
from .views import *

urlpatterns = [

        path('add-product/', AddProduct.as_view(), name='add-product'),
        path('user-products/', UserProducts.as_view(), name='user-products'),
        path('delete-product/', DeleteProduct.as_view(), name='delete-product'),
        path('update-product/', UpdateProduct.as_view(), name='update-product'),
]