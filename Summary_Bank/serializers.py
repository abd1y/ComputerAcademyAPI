from rest_framework import serializers
from .models import Summary_Bank
from .models import Departments_gategory
from authentication.models import Profile

class ProfileSerilazer(serializers.ModelSerializer):
    class Meta:
        model =Profile
        fields=['id','Name','Verified']
class Departments_gategory_Serilazer(serializers.ModelSerializer):
     class Meta:
        model =Departments_gategory
        fields=['Name_department','Short_code_department']
        
class Sumary_bank_Serilazer(serializers.ModelSerializer):
    Departments=Departments_gategory_Serilazer(many=True)
    user=ProfileSerilazer()
    class Meta:
        model =Summary_Bank
        fields=['id','Publish','File_name','File','Level','Course','Departments','user']