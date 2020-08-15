from django.db import models
from accounts.models import Account, Address
from products.models import Product


class Cart(models.Model):
    """A model that contains data for a shopping cart."""
    owner = models.OneToOneField(Account, related_name='cart', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s_cart' % self.owner.username


class CartItem(models.Model):
    """A model that contains data for an item in the shopping cart."""
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return '%s: %s' % (self.product.title, self.quantity)


class Order(models.Model):
    """
    An Order is the more permanent counterpart of the shopping cart. It represents
    the frozen state of the cart on the moment of a purchase. In other words,
    an order is a customer purchase.
    """
    owner = models.ForeignKey(Account, related_name='orders', on_delete=models.CASCADE, null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.ForeignKey(Address, related_name='orders', on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return '%s_order' % self.owner.username


class OrderItem(models.Model):
    """A model that contains data for an item in an order."""
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return '%s: %s' % (self.product.title, self.quantity)
