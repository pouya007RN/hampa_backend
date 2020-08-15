from django.core.paginator import Paginator
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import Product, Category, Comments, Rate, Likes
from .serializers import ProductSerializer, CategorySerializer, CommentSerializer, AddCommentSerializer
from accounts.models import Profile

PAGE_SIZE = 8


class ProductList(APIView):
    def get(self, request):
        query = Product.objects.all()

        if request.data.get('page'):
            page_number = request.data.get('page')
            paginator = Paginator(query, PAGE_SIZE)
            page_obj = paginator.get_page(page_number)
        else:
            paginator = Paginator(query, PAGE_SIZE)
            page_obj = paginator.get_page(1)

        serializer = ProductSerializer(page_obj, many=True)
        return Response(serializer.data)


class Categories(APIView):
    def get(self,request):
        query = Category.objects.all()
        serializer = CategorySerializer(query,many=True)
        return Response(serializer.data)

    def post(self,request):

        item = request.data.get('choice')
        filter = Product.objects.filter(tags__tag=item)

        if request.data.get('page'):
            page_number = request.data.get('page')
            paginator = Paginator(filter, PAGE_SIZE)
            page_obj = paginator.get_page(page_number)
        else:
            paginator = Paginator(filter, PAGE_SIZE)
            page_obj = paginator.get_page(1)

        serializer = ProductSerializer(page_obj, many=True)
        return Response(serializer.data)


class ProductSearch(APIView):
    def post(self, request):

        input = request.data.get('input')

        title = Product.objects.filter(title__icontains=input)
        tag = Product.objects.filter(tags__tag__icontains=input)
        detail = Product.objects.filter(detail__icontains=input)
        hashtags = Product.objects.filter(hashtags__icontains=input)

        result = title | tag | detail | hashtags

        if request.data.get('page'):
            page_number = request.data.get('page')
            paginator = Paginator(result, PAGE_SIZE)
            page_obj = paginator.get_page(page_number)
        else:
            paginator = Paginator(result, PAGE_SIZE)
            page_obj = paginator.get_page(1)

        serializer = ProductSerializer(page_obj, many=True)

        return Response(serializer.data)


class ProductDetail(APIView):

    def post(self, request):

        product = request.data.get('productID')
        detail = Product.objects.get(id=product)
        serializer = ProductSerializer(detail, many=False)
        return Response(serializer.data)


class CommentList(APIView):

    def post(self, request):
        product = request.data.get('productID')
        comments = Comments.objects.filter(product__id=product)

        serializer = CommentSerializer(comments, many=True)

        for key in serializer.data:
            key['date'] = key['date'][:10]

        for i in range(len(serializer.data)):

            like = Likes.objects.filter(comment__id=list(comments.values('id'))[i]['id']).filter(like='like').count()
            dislike = Likes.objects.filter(comment__id=list(comments.values('id'))[i]['id']).filter(like='dislike').count()
            image = Profile.objects.filter(user__id=list(comments.values('user'))[i]['user']).values('image')
            serializer.data[i]['like'] = like
            serializer.data[i]['dislike'] = dislike
            serializer.data[i]['profile'] = list(image)[0]
        return Response(serializer.data)


class AddComment(generics.CreateAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddCommentSerializer

    def perform_create(self, serializer):

        product_id = self.request.data.get("productID")
        text = self.request.data.get("text")
        user = self.request.user

        product = Product.objects.get(id=product_id)

        serializer.save(user=user, product=product, text=text)


class ProductRate(APIView):

    def post(self, request):

        product = request.data.get('productID')
        rate_num = Rate.objects.filter(product__id=product).count()
        rate_acc = Rate.objects.filter(product__id=product).aggregate(Sum('rate'))

        try:
            rate_avg = int(list(rate_acc.values())[0]) / rate_num

        except TypeError or ZeroDivisionError:
            rate_avg = 0

        json = dict()
        json['rate'] = rate_avg

        return Response(json)


class AddProductRate(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        product = request.data.get('productID')
        pro = Product.objects.get(id=product)
        rate = request.data.get('rate')
        json = dict()

        if Rate.objects.filter(product=product).filter(user=request.user).exists():
            json['error'] = True
            json['message'] = "User has already recorded a rate for this product"

            return Response(json)

        else:
            Rate.objects.create(user=request.user, product=pro, rate=rate)

            json['error'] = False
            json['message'] = 'You have successfully recorded your rate ({})'.format(rate)

            return Response(json)


class CheckRateRequest(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        product = request.data.get('productID')
        json = dict()

        if Rate.objects.filter(product=product).filter(user=request.user).exists():
            json['error'] = True
            json['message'] = "User has already recorded a rate for this product"

            return Response(json)

        else:
            json['error'] = False
            json['message'] = 'User can rate for this product'

            return Response(json)


class AddCommentLike(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        comment = request.data.get('commentID')
        cm = Comments.objects.get(id=comment)
        like = request.data.get('like')

        json = dict()

        if Likes.objects.filter(comment=comment).filter(user=request.user).exists():
            user_like = list(Likes.objects.filter(comment=comment).filter(user=request.user).values_list('like'))[0][0]
            print(type(like))
            if user_like == 'like' and like == 'like':
                json['error'] = True
                json['message'] = "User has already liked this comment"

                return Response(json)

            elif user_like == 'dislike' and like == 'dislike':

                json['error'] = True
                json['message'] = "User has already disliked this comment"

                return Response(json)

            elif user_like == 'like' and like == 'dislike':

                likes = Likes.objects.get(comment=comment, user=request.user)
                print(likes.like)
                likes.like = 'dislike'

                likes.save()

                like_num = Likes.objects.filter(comment__id=comment).filter(like='like').count()
                dislike_num = Likes.objects.filter(comment__id=comment).filter(like='dislike').count()

                json['error'] = False
                json['message'] = 'You have successfully {}d this comment'.format(like)
                json['like'] = like_num
                json['dislike'] = dislike_num

                return Response(json)

            elif  user_like == 'dislike' and like == 'like':

                likes = Likes.objects.get(comment=comment, user=request.user)
                likes.like = 'like'

                likes.save()

                like_num = Likes.objects.filter(comment__id=comment).filter(like='like').count()
                dislike_num = Likes.objects.filter(comment__id=comment).filter(like='dislike').count()

                json['error'] = False
                json['message'] = 'You have successfully {}d this comment'.format(like)
                json['like'] = like_num
                json['dislike'] = dislike_num

                return Response(json)

        else:
            Likes.objects.create(user=request.user, comment=cm, like=like)

            like_num = Likes.objects.filter(comment__id=comment).filter(like='like').count()
            dislike_num = Likes.objects.filter(comment__id=comment).filter(like='dislike').count()

            json['error'] = False
            json['message'] = 'You have successfully {}d this comment'.format(like)
            json['like'] = like_num
            json['dislike'] = dislike_num

            return Response(json)


class StaticUrl(APIView):
    def get(self, request):

        right = ['http://s11.picofile.com/file/8394813200/right1.jpg',
                 'http://s10.picofile.com/file/8394813300/right2.jpg',
                 'http://s10.picofile.com/file/8394813368/right3.jpg',
                 'http://uupload.ir/files/3xm9_start.png']

        left = 'http://s10.picofile.com/file/8394813134/left.jpg'

        json = dict()
        json['left'] = left
        json['right'] = right

        return Response(json)


class CheckUserLike(APIView):

    def post(self, request):

        comment = request.data.get('commentID')
        json = dict()
        json['like'] = False
        json['dislike'] = False
        json['none'] = False
        if Likes.objects.filter(comment=comment).filter(user=request.user).exists():

            user_like = list(Likes.objects.filter(comment=comment).filter(user=request.user).values_list('like'))[0][0]

            if user_like == 'like':

                json['like'] = True
                return Response(json)

            elif user_like == 'dislike':

                json['dislike'] = True
                return Response(json)
        else:

            json['none'] = True
            return Response(json)


class SimilarProducts(APIView):

    def post(self, request):

        productID = request.data.get('productID')
        product_hashtags = Product.objects.get(id=productID).hashtags
        hashtags_list = str(product_hashtags).split(', ')

        similar1 = Product.objects.filter(hashtags__icontains=hashtags_list[0])
        similar2 = Product.objects.filter(hashtags__icontains=hashtags_list[1])
        similar3 = Product.objects.filter(hashtags__icontains=hashtags_list[2])
        similar4 = Product.objects.filter(hashtags__icontains=hashtags_list[3])
        similar5 = Product.objects.filter(hashtags__icontains=hashtags_list[4])
        similar6 = Product.objects.filter(hashtags__icontains=hashtags_list[5])
        similar7 = Product.objects.filter(hashtags__icontains=hashtags_list[6])
        similar8 = Product.objects.filter(hashtags__icontains=hashtags_list[7])

        similar = similar1 | similar2 | similar3 | similar4 | similar5 | similar6 | similar7 | similar8

        serializer = ProductSerializer(similar, many=True)

        return Response(serializer.data)


class TotalCatProducts(APIView):

    def post(self, request):

        cat = request.data.get('cat')
        if cat == 'all':
            total = Product.objects.all().count()
        else:
            total = Product.objects.filter(tags__tag=cat).count()
        json = {'product_number': total}
        return Response(json)


class TotalSearchProducts(APIView):

    def post(self, request):

        inp = request.data.get('input')
        if inp is None:
            total = Product.objects.all().count()
        else:
            title = Product.objects.filter(title__icontains=inp)
            tag = Product.objects.filter(tags__tag__icontains=inp)
            detail = Product.objects.filter(detail__icontains=inp)
            hashtags = Product.objects.filter(hashtags__icontains=inp)

            result = title | tag | detail | hashtags

            total = len(result)

        json = {'product_number': total}
        return Response(json)
