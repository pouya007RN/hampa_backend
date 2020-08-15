from rest_framework import serializers
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):


    class Meta:

        model = Product

        fields = '__all__'


class ProductReadSerializer(serializers.ModelSerializer):

    tags = serializers.StringRelatedField(many=True)

    class Meta:

        model = Product

        fields = ('id', 'title', 'price', 'image', 'URL', 'tags', 'owner', 'count', 'detail')

