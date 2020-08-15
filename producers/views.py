from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from accounts.permissions import IsOwnerOrReadOnly
from products.models import *
from .serializers import *
import requests

api_key = 'acc_bc66de9c9f82019'
api_secret = '6f542c4c62a6d211f67cd42e6e0238f5'


class AddProduct(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        owner = Account.objects.get(username=self.request.user)
        title = self.request.data.get('title')
        if self.request.FILES:
            image = self.request.data['image']
        else:
            image = None
        price = self.request.data.get('price')
        detail = self.request.data.get('detail')
        tags = self.request.data.get('tags')
        count = self.request.data.get('count')

        pro = serializer.save(owner=owner, title=title, price=price, detail=detail, tags=tags, count=count, image=image)
        image_path = "/home/pouya007/Desktop/hampa-backed/media/" + str(image)

        response = requests.post(
            'https://api.imagga.com/v2/tags',
            auth=(api_key, api_secret),
            files={'image': open(image_path, 'rb')}).json()

        hashtag = []
        for i in range(8):
            hashtag.append(response['result']['tags'][i]['tag']['en'])
        cast_string = ''
        for i in (str(hashtag)[1:-1:1]):
            if i is not "'":
                cast_string += i

        pro.hashtags = cast_string
        pro.save()


class UserProducts(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request):
        products = Product.objects.filter(owner=request.user)
        serializer = ProductReadSerializer(products, many=True)

        for i in range(len(serializer.data)):

            rate_num = Rate.objects.filter(product__id=list(products.values('id'))[i]['id']).count()
            rate_acc = Rate.objects.filter(product__id=list(products.values('id'))[i]['id']).aggregate(Sum('rate'))

            try:
                rate_avg = int(list(rate_acc.values())[0]) / rate_num

            except TypeError or ZeroDivisionError:
                rate_avg = 0

            serializer.data[i]['rate'] = rate_avg

        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get('productID')
        product = Product.objects.get(owner=request.user, id=product_id)
        serializer = ProductReadSerializer(product, many=False)

        return Response(serializer.data)


class DeleteProduct(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request):
        product_id = request.data.get('productID')
        product = Product.objects.get(owner=request.user, id=product_id)

        product.delete()
        return Response({'message': 'Product number {} successfully deleted.'.format(product_id)})


class UpdateProduct(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def put(self, request):

        title = request.data.get('title')
        if request.FILES:
            image = request.data['image']
        else:
            image = None
        price = request.data.get('price')
        detail = request.data.get('detail')
        tags = request.data.get('tags')
        count = request.data.get('count')

        product = Product.objects.get(owner=request.user, id=request.data.get('productID'))

        product.title = title
        if request.FILES:
            product.image = image
            image_path = "/home/pouya007/Desktop/hampa-backed/media/" + str(image)

            response = requests.post(
                'https://api.imagga.com/v2/tags',
                auth=(api_key, api_secret),
                files={'image': open(image_path, 'rb')}).json()

            hashtag = []
            for i in range(8):
                hashtag.append(response['result']['tags'][i]['tag']['en'])
            cast_string = ''
            for i in (str(hashtag)[1:-1:1]):
                if i is not "'":
                    cast_string += i

            product.hashtags = cast_string

        product.price = price
        product.count = count
        product.detail = detail
        if type(tags) is int:
            product.tags.set([tags])
        else:
            product.tags.set(tags)

        product.save()

        serializer = ProductReadSerializer(product, many=False)
        return Response(serializer.data)
