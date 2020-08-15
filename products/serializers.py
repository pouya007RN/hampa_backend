from rest_framework import serializers
from .models import Product, Category, Comments
from accounts.serializers import AccountSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category

        fields = ('id', 'tag', 'URL', 'image',)


class ProductSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product

        fields = ('id', 'title', 'price', 'image', 'URL', 'tags', 'owner', 'count', 'detail', 'hashtags')


class CommentSerializer(serializers.ModelSerializer):
    user = AccountSerializer()

    class Meta:
        model = Comments

        fields = ('id', 'user', 'product', 'text', 'date')


class AddCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments

        fields = ('id', 'text')


class ProductReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments

        fields = '__all__'
