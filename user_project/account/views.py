from django.contrib.auth.password_validation import validate_password
from django.contrib.sites import requests
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse
from rest_framework.views import Response
from .serializers import RegistrationSerializer, LoginSerializers, ResetPasswordSerializer
from django.contrib.auth import get_user_model, authenticate, login, logout, get_user
from rest_framework import permissions, generics

from .token_operations import get_token, get_data, Common

User = get_user_model()


class RegistrationApiView(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        """
        post api is for user registration for registering new users
        :return: message after validations for adding new user
        """
        req_data = request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        first_name = req_data.get('first_name')
        last_name = req_data.get('last_name')
        username = req_data.get('username')
        email = req_data.get('email')
        password = req_data.get('password')
        confirm_password = req_data.get('confirm_password')
        try:
            query = User.objects.filter(Q(email__iexact=email))
            if query.exists():
                return HttpResponse('user already exists')

            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                            email=email)
            # print(user)
            user.set_password(password)
            user.is_active = False
            user.save()
            current_site = get_current_site(request).domain
            token = get_data(user).get('access')
            short_token = Common.token_encode(token)
            link = reverse('activate')
            surl = 'http://' + current_site + link + '?token=' + short_token

            return Response({"msg": "User Created Successfully and activate link to activate the account", 'code': 200,
                             'activate link': surl})
        except Exception as e:
            return Response({"msg": "Oops! Something went wrong, please try again later.", "error": e})


class LoginApiView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializers

    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializers(data=data)
            serializer.is_valid(raise_exception=True)
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if not user:
                return Response({'Error': 'Invalid email or password', 'code': 401})
            login(request, user)
            token = get_token(user)
            return Response({'msg': 'User Logged in Successfully', 'code': 200, 'token': token})

        except Exception:
            return Response({'msg': 'Oops! Something went wrong, please try again later', 'code': 400})


class ActivateApiView(generics.GenericAPIView):
    def get(self, request):
        user_data = get_data(request)
        user = User.objects.get(user_data)
        user.is_active = True
        user.save()
        return Response({'msg': 'User Account is activated successfully', 'code': 200})


class LogoutApiView(generics.GenericAPIView):
    def get(self, request):
        logout(request)
        return Response({'msg': 'User Logged Out Successfully', 'code': 200})


class ResetPasswordApiView(generics.GenericAPIView):
    authentication_classes = ()
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        data = request.data
        serializer = ResetPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(username=data.get('username'))
        user.set_password(data.get('new_password'))
        user.save()
        return Response({'msg': 'New password Updated Successfully', 'code': 200})
