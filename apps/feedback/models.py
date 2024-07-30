from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    feedback = models.TextField()  # Ensure this field exists
    email = models.EmailField()  # Ensure this field exists
    created_at = models.DateTimeField(auto_now_add=True)  # Ensure this field exists

    def __str__(self):
        return self.name
