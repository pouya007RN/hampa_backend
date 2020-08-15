from django.contrib import admin
from .models import Product, Category, Comments, Rate, Likes

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(Rate)
admin.site.register(Likes)
