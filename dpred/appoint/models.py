from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class appointment(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=200, null=False)
    dog_breed = models.CharField(max_length=200, null=False)
    age = models.IntegerField(max_length=200, null=False)
    vet_id = models.IntegerField(max_length=200, null=False)
    desc = models.CharField(max_length=500, null=True)
    user_id = models.IntegerField(null=False)
    date = models.DateField(null=False)
    phone = models.IntegerField(max_length=10, null=False)
    time = models.TimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.IntegerField(default=0)
    doc_desc = models.CharField(max_length=500, null=True, default="-")
    roomid=  models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
