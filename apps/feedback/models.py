from django.db import models

class Feedback(models.Model):
    feedback = models.TextField()
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.feedback[:50]  # Display the first 50 characters of feedback
