from rest_framework import serializers
from cart.models import *
from products.serializers import ProductSerializer
from accounts.serializers import AddressSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'owner', 'created_at', 'updated_at', 'cart_items']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'status']


class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    order_items = OrderItemSerializer(many=True, required=False)
    address = AddressSerializer(many=False, required=False)

    class Meta:
        model = Order
        fields = ['id', 'owner', 'total', 'created_at', 'updated_at', 'order_items', 'address', 'status']
