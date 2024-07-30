from django.db import models

class Feedback(models.Model):
    feedback = models.TextField()  # To store the feedback text
    email = models.EmailField()    # To store the user's email address
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the date and time when the feedback is created

    def __str__(self):
        return self.feedback[:50]  # Display the first 50 characters of feedback in the admin interface
