from django.urls import path
from .views import feedback_view

urlpatterns = [
    path('feedback/', feedback_view, name='feedback'),
    path('feedback/thanks/', TemplateView.as_view(template_name='feedback_thanks.html'), name='feedback_thanks'),
    # Other URL patterns...
]
