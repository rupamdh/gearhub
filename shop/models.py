from typing import Iterable
from django.db import models
from django.utils.text import slugify
from account.models import User

# Create your models here.
class ServiceCenter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=400)
    slug = models.SlugField(max_length=500, null=True, blank=True, unique=True, editable=False)
    

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    

class Service(models.Model):
    title = models.CharField(max_length=300)
    details = models.TextField()
    center = models.ForeignKey(ServiceCenter, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.center.name} - {self.title}'