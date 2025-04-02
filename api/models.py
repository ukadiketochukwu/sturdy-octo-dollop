from django.db import models
from django.contrib.auth.models import User

# Doctor model
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.user.username} ({self.specialty})"

# Patient model
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"Patient: {self.user.username}"
