from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

def validate_unique_username(value):
    if CustomUser.objects.filter(username=value).exists():
        raise ValidationError('Пользователь с таким именем уже существует.')

class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message='Введите корректный email')]
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.username
    