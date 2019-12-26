from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from accounts.api.serializers import AccountRegistraitionSerializer, AccountSerializer
from accounts.models import Account
from rest_framework.permissions import IsAuthenticated, AllowAny
import requests as rq


class RegistrationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AccountRegistraitionSerializer

    def post(self, *args):
        serializer = AccountRegistraitionSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            user = User(
                username=self.request.data['username'],
                first_name=self.request.data['first_name'],
                last_name=self.request.data['last_name'],
                email=self.request.data['email'],
            )
            user.set_password(self.request.data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # If you want to use Hunter Email verification you need to uncomment code below!!!!

    # def post(self, *args):
    #     response = rq.get(
    #         'https://api.hunter.io/v2/email-verifier',
    #         params={
    #             'email': self.request.data['email'],
    #             'api_key': 'your_api_key'  # Enter API key here!!
    #         }
    #     )
    #     if response['data']['result'] == 'deliverable':
    #         serializer = AccountRegistraitionSerializer(data=self.request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             user = User(
    #                 username=self.request.data['username'],
    #                 first_name=self.request.data['first_name'],
    #                 last_name=self.request.data['last_name'],
    #                 email=self.request.data['email'],
    #             )
    #             user.set_password(self.request.data['password'])
    #             user.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({'response': 'Email was not verified!'})


class UsersList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer

    def get_queryset(self):
        if 'email' in self.request.data:
            response_ = get_object_or_404(Account, email=self.request.data['email'])
            serializer = AccountSerializer(response_)
        else:
            response_ = Account.objects.all()
            serializer = AccountSerializer(response_, many=True)
        return response_


class UserDetail(generics.GenericAPIView):
    lookup_field = 'email'
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        account = get_object_or_404(Account, email=kwargs['email'])
        return Response(self.serializer_class(account).data)
