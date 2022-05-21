from django.urls import path

from . import views

urlpatterns = [
    path('blog/', views.PostListCreateView.as_view()),
    path('blog/<int:post_id>/', views.PostInstanceView.as_view()),
]
