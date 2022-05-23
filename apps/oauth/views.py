from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from .models import User
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, UserSerializer


class TokenObtainPairView(TokenViewBase):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    authentication_classes = []
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(email=response.data.get('email'))
        refresh_token = MyTokenObtainPairSerializer.get_token(user)
        return Response({
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token),
        }, status=status.HTTP_201_CREATED)


class UserView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        if not self.request.user.is_authenticated:
            self.permission_denied(self.request, 'Permission Denied', 401)
        else:
            return self.request.user
