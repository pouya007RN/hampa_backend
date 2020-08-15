from rest_framework import serializers
from accounts.models import Account, Profile, Address


class AccountSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        account = Account.objects.create(**validated_data)
        account.set_password(validated_data['password'])
        account.save()
        return account

    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'is_producer')
        extra_kwargs = {'password': {'write_only': True}}


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ['id', 'province', 'city', 'address']


class ProfileSerializer(serializers.ModelSerializer):
    user = AccountSerializer(many=False, read_only=True)
    addresses = AddressSerializer(many=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'created_at', 'updated_at', 'addresses', 'image', 'credit')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.user.save()
        instance.save()
        return instance
