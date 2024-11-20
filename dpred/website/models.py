from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class veterinarian(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=200, null=False)
    username = models.CharField(max_length=200, null=False, unique=True)
    password = models.CharField(max_length=200, null=False)
    profile_pic = models.ImageField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    rating= models.IntegerField(null= True, blank=True)
    feedback= models.CharField(max_length=500, null=True, default="-")

    def __str__(self):
        return self.username
    
class feedback(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    user_id = models.IntegerField(null= True, blank=True)
    username = models.CharField(max_length=200, null=False, unique=True)
    rating= models.IntegerField(null= True, blank=True)
    feedback= models.CharField(max_length=500, null=True, default="-")
    
    def __str__(self):
        return self.username
    
