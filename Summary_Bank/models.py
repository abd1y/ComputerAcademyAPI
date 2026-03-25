from django.db import models
from django.contrib.auth.models import User
from authentication.models import Profile
# Create your models here.

class Departments_gategory(models.Model):
    Name_department=models.CharField(unique=True)
    Short_code_department=models.CharField(unique=True)
    def __str__(self):
        return self.Name_department
class Summary_Bank(models.Model):
    STAGE_CHOICES=[
        ("1",1),    
        ("2",2),
        ("3",3),
        ("4",4),
    ] 
    COURSE_CHOICE=[
        ("1",1),
        ("2",2),
    ]
    user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    File_name=models.TextField(null=False,blank=False)
    File=models.FileField(upload_to='Summary_Bank_file/',null=False,blank=False)
    Departments=models.ManyToManyField(Departments_gategory,null=False,blank=False)
    Level=models.CharField(choices=STAGE_CHOICES,null=False,blank=False)
    Course=models.CharField(choices=COURSE_CHOICE,null=False,blank=False)
    Publish=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.File_name} - {self.Publish}"