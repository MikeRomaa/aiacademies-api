from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.oauth.urls')),
    path('api/', include('apps.courses.urls')),
    path('api/', include('apps.blog.urls')),
    path('api/', include('apps.feedback.urls')),
    path('admin/', admin.site.urls),
]
