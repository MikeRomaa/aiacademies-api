from django.urls import path
from .views import FeedbackListCreateAPIView, FeedbackDetailAPIView

urlpatterns = [
    path('feedback/', FeedbackListCreateAPIView.as_view(), name='feedback-list-create'),
    path('feedback/<int:pk>/', FeedbackDetailAPIView.as_view(), name='feedback-detail'),
]
