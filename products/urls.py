from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('static-url/', StaticUrl.as_view(), name='static'),
    path('category/', Categories.as_view(), name='categories'),
    path('search/', ProductSearch.as_view(), name='search'),
    path('product-detail/', ProductDetail.as_view(), name='details'),
    path('comments/', CommentList.as_view(), name='comments'),
    path('add-comment/', AddComment.as_view(), name='add-comment'),
    path('rate/', ProductRate.as_view(), name='rate'),
    path('add-rate/', AddProductRate.as_view(), name='add-rate'),
    path('check-rate/', CheckRateRequest.as_view(), name='check-rate'),
    path('add-likes/', AddCommentLike.as_view(), name='add-likes'),
    path('check-likes/', CheckUserLike.as_view(), name='check-likes'),
    path('similar-products/', SimilarProducts.as_view(), name='similar-products'),
    path('total/', TotalCatProducts.as_view()),
    path('total-search/', TotalSearchProducts.as_view()),
]
