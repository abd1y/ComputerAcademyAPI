from rest_framework.authtoken.models import Token

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Profile(models.Model):
 user=models.OneToOneField(User,on_delete=models.CASCADE)
 Name=models.CharField(max_length=150)
 Profile_image=models.ImageField(upload_to='profile_images/',default='profile_images/defuld.jpg')
 Bio=models.TextField(max_length=250,blank=True,default="")
 Verified=models.BooleanField(default=False)
 Activ=models.BooleanField(default=False)
 Email_code=models.TextField(null=True,blank=True)
 def __str__(self):
     return self.Name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Token.objects.create(user=instance)
        
