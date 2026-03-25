from .models import Group,Post,Comment
from django.contrib.auth.models import User
from rest_framework import serializers
import mimetypes

class Groups(serializers.ModelSerializer):
    
    class Meta:
        model=Group
        fields = '__all__'
      
class CommentSer(serializers.ModelSerializer):
     member_name=serializers.CharField(source='member.user.first_name',read_only=True)
     Profile_image=serializers.ImageField(source='member.user.profile.Profile_image',read_only=True)
     user_id=serializers.IntegerField(source='member.user.id',read_only=True)
     Comment_id = serializers.IntegerField(source='id', read_only=True)
     class Meta:
        model = Comment   
        fields =['user_id','Comment_id','member_name','Profile_image','content'] 
        
        
        
        
class PostSer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source='id', read_only=True)
    member_profile=serializers.ImageField(source='member.user.profile.Profile_image', read_only=True)
    member_name=serializers.CharField(source='member.user.first_name', read_only=True)
    user_id=serializers.IntegerField(source='member.user.id',read_only=True)
    role = serializers.CharField(source='member.role', read_only=True)
    Totle_comment=serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comment=CommentSer(many=True, read_only=True)
    class Meta:
        model=Post
        fields=['post_id','user_id','member_name','member_profile','role','title','media','Like','is_liked','Totle_comment','comment']
    def get_Totle_comment(self, obj):
        return obj.comment.count()
    def get_is_liked(self, obj):
        request = self.context.get('request')  
        if request and hasattr(request, "user"):
            return request.user in obj.by_like.all()
        return False
 
       
        
        