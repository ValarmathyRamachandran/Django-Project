from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.views import Response
from .serializers import RegistrationSerializer, LoginSerializers
from django.contrib.auth import get_user_model, authenticate, login
from rest_framework import permissions, generics

User = get_user_model()


class RegistrationAPIView(generics.GenericAPIView):
    permission_classes = ()
    serializer_class = RegistrationSerializer
    authentication_classes = ()

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
            validate_email(email)
        except ValidationError:
            return Response('Please enter valid email')
        query = User.objects.filter(
            Q(username__iexact=username))

        if query.exists():
            return HttpResponse('user already exists')

        if password != confirm_password:
            return HttpResponse('password did not match')
        try:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email)
            print(user)
            user.set_password(password)
            user.is_active = False
            user.save()
            print("hi", user)
            return HttpResponse("User Created Successfully", user)
        except Exception as e:
            return HttpResponse("Oops! Something went wrong, please try again later.", e)


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
            # print(user)

            if not user:
                return Response({'Error': 'Invalid email or password', 'code': 401})
            login(request, user)
            return Response({'msg': 'User Logged in Successfully', 'code': 200})

        except Exception:
            return HttpResponse("Oops! Something went wrong, please try again later")
