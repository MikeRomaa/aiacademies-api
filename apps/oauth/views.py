from rest_framework_simplejwt.views import TokenViewBase

from .serializers import MyTokenObtainPairSerializer


class TokenObtainPairView(TokenViewBase):
    serializer_class = MyTokenObtainPairSerializer
