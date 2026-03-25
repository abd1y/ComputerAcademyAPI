from django.db import models
from django.core.validators import MinLengthValidator
# Create your models here.
from django.db import models
from  django.contrib.auth.models import User
import random, string

def get_code_Group():
    chars=string.ascii_uppercase + string.digits
    return '#' + ''.join(random.choice(chars) for _ in range(6))



#  Main Groups
class Group(models.Model):
    
    STAGE_CHOICES=[
        ("1",1),    
        ("2",2),
        ("3",3),
        ("4",4),
    ]
    group_name=models.CharField(max_length=26,null=False,blank=False)
    Level=models.CharField(max_length=7,choices=STAGE_CHOICES)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='owned_groups')
    Group_code=models.CharField(max_length=7,unique=True,default=get_code_Group)
    allow_post=models.BooleanField(default=True)
    allow_comments=models.BooleanField(default=True)
    
    def __str__(self):
        return self.group_name

# Member

class Member(models.Model):
    Role=[
        ('admin','Admin'),
        ('member',"Member")
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    group=models.ForeignKey(Group,on_delete=models.CASCADE) 
    role=models.CharField(max_length=10,default='member' ,choices=Role)  
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return f"{self.user.first_name} - {self.group.group_name}"
    class Meta:
        unique_together = ('user','group')
       
       
       
 #Post 
class Post(models.Model):
    member=models.ForeignKey(Member,on_delete=models.CASCADE)
    title=models.TextField(null=False,blank=False)
    media =models.FileField(upload_to='Post_Group/',null=True,blank=True)
    Like=models.IntegerField(default=0)
    by_like=models.ManyToManyField("auth.User",blank=True,related_name='by_like')
    def __str__(self):
       return f"{self.member.user.first_name} :  {self.member.group.group_name} "
# comment
class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comment')
    member=models.ForeignKey(Member,on_delete=models.CASCADE)
    content =models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.member.user.first_name}"
    class Meta:
        ordering = ['-created_at']
   