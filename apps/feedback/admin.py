from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'feedback', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('feedback', 'email')
    ordering = ('-created_at',)  # Orders by creation date, newest first
