from django.urls import path
from accounts.views import UserCreate, UserLogout, UserInfo, Ticket
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', UserCreate.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login_refresh'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('retrieve/', UserInfo.as_view(), name='retrieve'),
    path('ticket/', Ticket.as_view(), name='ticket'),
]
