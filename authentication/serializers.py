from .models import Profile
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class Singup(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields=['id','first_name','email','password']
        extra_kwargs={
            'first_name':{
                'required': True,
                'allow_blank': False,
            },
            'email':{
                'required': True,
                'allow_blank': False,
                'validators': [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message='is existing'
                    )
                ]
                
            },
            'password':{
                'required': True,
                'allow_blank': False,
                'min_length': 8,
            },
        }
class LongIn(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['email','password']
