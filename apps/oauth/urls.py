from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    path('token/', views.TokenObtainPairView.as_view()),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('user/', views.UserView.as_view()),
]
