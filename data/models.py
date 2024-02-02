# models.py in your_app

from django.db import models

class User(models.Model):
    mobile_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # Add other fields as needed

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # Add other methods or fields as needed
