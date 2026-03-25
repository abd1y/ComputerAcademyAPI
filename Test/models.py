from django.db import models

# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    bio=models.TextField(null=True, blank=True)
    picture=models.ImageField(upload_to='images/', null=True, blank=True)   