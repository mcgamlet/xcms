from django.db import models
from django.contrib.auth.models import User, UserManager
from xcms.VM.models import VM

class CustomUser(User,models.Model):

    """User with app settings."""
    #timezone = models.CharField(max_length=50, default='Europe/London')
    core_num=models.IntegerField(default=1)
    mem_limit=models.IntegerField(default=256)
    vms=models.ManyToManyField(VM)
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

# Create your models here.
