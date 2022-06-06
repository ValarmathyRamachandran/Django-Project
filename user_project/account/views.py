import generics as generics
from rest_framework.views import APIView, Response
from rest_framework import generics
from .serializers import RegistrationSerializer, LoginSerializers
from django.contrib.auth import get_user_model, authenticate, login

User = get_user_model()


class RegistrationAPIView(generics.GenericAPIView):

    def post(self, request):
        """
        post api is for user registration for registering new users
        :return: message after validations for adding new user
        """
        req_data = request.data
        serializer = RegistrationSerializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        first_name = serializer.data.get('first_name')
        last_name = serializer.data.get('last_name')
        username = serializer.data.get('username')
        email = serializer.data.get('email')
        password = serializer.data.get('password')

        user = User.objects.create_user(first_name=first_name, last_name=last_name,
                                        username=username, email=email, password=password)
        # if User.objects.filter(email=user.email):
        # return Response({'msg': 'User Already exists'})
        user.save()
        return Response({'msg': 'User Registered successfully', 'code': 200})


class LoginApiView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        data = request.data
        serializer = LoginSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        print(type(username))
        print(password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if not user:
            return Response({'Error': 'Invalid email or password', 'Code': 401})
        login(request, user)
        return Response({'msg': 'User Logged in Successfully', 'Code': 200})
