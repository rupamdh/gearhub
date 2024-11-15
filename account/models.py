from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email Must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)
    


class User(AbstractUser):
    username = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_password(self.password)
        return super().save(*args, **kwargs)
    
    def get_centers(self):
        from shop.models import ServiceCenter
        centers = ServiceCenter.objects.filter(user=self)
        return centers
        

    def get_total_center(self):
        from shop.models import ServiceCenter
        centers = ServiceCenter.objects.filter(user=self).count()
        return centers
        
    


class Wallet(models.Model):
    TYPE_CHOICE = (
        ('CR', 'Credit'),
        ('DB', 'Debit')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallet_user')
    type = models.CharField(max_length=2, choices=TYPE_CHOICE)
    amount = models.IntegerField()
    remark = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.user.email
    
