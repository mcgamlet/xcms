from django.db import models

class VM(models.Model):
    name=models.CharField(max_length=100)
    vmr=models.CharField(max_length=100)


# Create your models here.
