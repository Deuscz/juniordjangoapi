from rest_framework import serializers
from accounts.models import Account


class AccountRegistraitionSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        account = Account(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        if validated_data['password'] != validated_data['password2']:
            raise serializers.ValidationError({'password': 'Your passwords must match!'})
        account.set_password(validated_data['password'])
        account.save()
        return account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name']