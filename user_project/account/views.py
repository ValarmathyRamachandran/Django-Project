import json
from django.contrib import messages
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from user_project.account.models import Account
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegistrationAPIView(GenericAPIView):
    @permission_classes((permissions.AllowAny,))
    def post(self, request):
        """
        post api is for user registration for this app
        :return: message after validations for adding new user
        """
        req_data = request.data
        print(request.data)
        record = json.loads(req_data)
        del record['confirm_password']
        account = Account(id=record['id'], first_name=record['first_name'], last_name=record['last_name'],
                          user_name=record['user_name'], email=record['email'], password=record['password'])
        if Account.objects.filter(email=account.email):
            return {'msg': 'User Already exists'}
        account.save()
        messages.success(request, f'Your account has been created! You are now able to log in')
        return {'msg': 'User Registered successfully'}, 200
