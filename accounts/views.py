from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets, generics
from rest_framework.decorators import action
from accounts.serializers import AccountSerializer, ProfileSerializer, AddressSerializer
from .models import Profile, Address
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsOwnerOrReadOnly
from hampa.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


class UserCreate(APIView):
    def post(self, request, format='json'):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            if user:
                json = serializer.data
                json['message'] = "Successfully Signed Up!"
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format='json'):
        token = RefreshToken(request.data.get("refresh"))
        token.blacklist()
        json = {'message': "Logged Out Successfully!"}
        return Response(json, status=status.HTTP_200_OK)


class UserInfo(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format='json'):
        serializer = AccountSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(detail=True, methods=['post', 'put'])
    def update_profile(self, request, pk=None):
        """update a user's profile"""

        profile = Profile.objects.filter(user=request.user).first()
        profile.user.username = request.data.get('username')
        profile.user.first_name = request.data.get('first_name')
        profile.user.last_name = request.data.get('last_name')
        profile.user.email = request.data.get('email')
        profile.user.phone_number = request.data.get('phone_number')
        if request.data.get('password'):
            profile.user.set_password(request.data.get('password'))
        if request.FILES:
            profile.image = request.data['image']

        profile.user.save()
        profile.save()

        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    @action(detail=False)
    def retrieve_profile(self, request):
        """return a user's profile"""

        profile = Profile.objects.filter(user=request.user).first()
        serializer = ProfileSerializer(profile)

        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def remove_profile(self, request, pk=None):
        """remove a user's profile"""

        profile = Profile.objects.filter(user=request.user).first()
        profile.user.delete()
        profile.delete()

        json = {'message': "Account deleted successfully!"}
        return Response(json, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'put'])
    def add_credit(self, request, pk=None):
        """increase a user profile's credit"""

        additional_credit = int(request.data.get('additional_credit'))
        profile = Profile.objects.filter(user=request.user).first()
        profile.credit += additional_credit
        profile.save()

        json = {'message': "Additional credit added successfully!"}
        return Response(json, status=status.HTTP_200_OK)


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['put'])
    def add_address(self, request, pk=None):
        profile = Profile.objects.filter(user=request.user).first()
        province = request.data.get('province')
        city = request.data.get('city')
        address = request.data.get('address')
        address_obj = Address(profile=profile, province=province, city=city, address=address)
        address_obj.save()

        serializer = AddressSerializer(address_obj)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def edit_address(self, request, pk=None):
        try:
            address_obj = Address.objects.get(pk=request.data.get('address_id'))
        except Exception as e:
            print(e)
            json = {'message': "No address with the given id exists!"}
            return Response(json, status=status.HTTP_400_BAD_REQUEST)
        address_obj.province = request.data.get('province')
        address_obj.city = request.data.get('city')
        address_obj.address = request.data.get('address')
        address_obj.save()

        serializer = AddressSerializer(address_obj)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def remove_address(self, request, pk=None):
        try:
            address_obj = Address.objects.get(pk=request.data.get('address_id'))
        except Exception as e:
            print(e)
            json = {'message': "No address with the given id exists!"}
            return Response(json, status=status.HTTP_400_BAD_REQUEST)

        address_obj.delete()

        json = {'message': "Address deleted successfully!"}
        return Response(json, status=status.HTTP_200_OK)


class Ticket(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request):

        subject = request.data.get('subject')
        context = request.data.get('context')

        send_mail(subject, context, EMAIL_HOST_USER, ['seydal6583@gmail.com'], fail_silently=False)

        return Response({'message': 'Ticket successfully composed.'})

