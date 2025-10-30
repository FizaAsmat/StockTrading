from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Users(models.Model):
    Role_Choices = [
        ('trader', 'trader'),
        ('admin', 'admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20,choices=Role_Choices,default='Trader')
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.role}'