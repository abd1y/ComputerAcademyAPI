from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from Summary_Bank.models import Summary_Bank
from .models import Profile
from .serializers import Singup,LongIn
from django.core.mail import send_mail
from rest_framework import status
import random
import resend 
from django.conf import settings
@api_view(['POST'])
@permission_classes([AllowAny])
def SingIn(req):
    SingupSer=Singup(data=req.data)
    code=str(random.randint(100000,999999))
    if not SingupSer.is_valid():
        return Response({"error": SingupSer.errors},status=status.HTTP_400_BAD_REQUEST)
    else:
        password=req.data['password']
        email=req.data['email']
        if email.startswith('cs') and email.endswith('@student.uotechnology.edu.iq'):
            verified=False
        elif email.endswith('@uotechnology.edu.iq'):
            verified=True
        else:
             return Response({"error":"The entered email is not a university email belonging to a student or a professor in the College of Computer Science."},status=status.HTTP_400_BAD_REQUEST)
        
        
    

        user=User.objects.create_user(
            first_name=req.data['first_name'],
            email=email,
            password=password,
            username=req.data['email'],
        )
        
        Profile=user.profile
        Profile.Verified=verified
        Profile.Name=user.first_name
        Profile.Email_code=code
       
        
        user.profile.save()
        html_contex=f"""
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>Verification Code</title>
</head>
<body style="margin:0; padding:0; background-color:#57595B; font-family:Arial, sans-serif; color:#fff;">
    <!-- رأس الرسالة -->
    <table width="100%" cellspacing="0" cellpadding="0" style="background-color:#2b2b2c; height:80px;">
        <tr>
            <td align="center">
                <table width="600" cellspacing="0" cellpadding="0">
                    <tr>
                        <td align="left" style="padding:10px;">
                            <img src="https://i.ibb.co/PzfXzcMQ/Logo.png" alt="Logo" width="50" height="50" style="display:block;" />
                        </td>
                        <td align="left" style="padding-left:10px; color:#ffffff; font-weight:bold; font-size:20px;">
                            Computer Academic
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>

    <!-- محتوى الرسالة -->
    <table width="100%" cellspacing="0" cellpadding="0">
        <tr>
            <td align="center" style="padding:40px 0;">
                <table width="600" cellspacing="0" cellpadding="0" style="background-color:#0F172A; border-radius:10px; padding:30px;">
                    <tr>
                        <td align="center">
                            <h1 style="color:gold; margin-bottom:20px;">مرحبا {user.profile.Name}</h1>
                            <p style="text-align:center; margin-bottom:20px;">
                        سعيد بانضمام طالب جديد إلى منصتنا Computer Academic كادر 
                            </p>
                            <p style="text-align:center; margin-bottom:30px;">
                                باقي خطوات قليلة لتصبح مستخدم رسمي في منصتنا<br>
                                كل ما عليك الآن فعله هو إدخال رمز التحقق أدناه
                            </p>
                            <h2 style="background-color:#333; color:#fff; padding:20px; border-radius:10px; display:inline-block; font-size:24px;">
                                {code}
                            </h2>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
        """
        resend.api_key = settings.RESEND_API_KEY
        resend.Emails.send({
        "from": "Computer Academic <codeprogram2003@gmail.com>",
        "to": [user.email],
        "subject": "رمز تحقق ",
        "html": html_contex
    })
        return Response({"Mesage":"تم انشاء حساب  بنجاح الان قم بتأكيد حسابك   ",       
            },status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def Longin(req):
    LongInSer=LongIn(data=req.data)
    if not LongInSer.is_valid():
        return Response({"البريد الالكتروني او كلمة السر خطأ"},status=status.HTTP_404_NOT_FOUND)
    else:
        email=LongInSer.validated_data['email']
        password=LongInSer.validated_data['password']
        user=User.objects.filter(email=email).first()
        password=check_password(password,user.password)
        if  not user or not password:
            return Response({"البريد الالكتروني او رمز سري خاطئ"},status=status.HTTP_404_NOT_FOUND)
         
        token,create=Token.objects.get_or_create(user=user)
        if not user.profile.Activ:
            return Response({"Erorr":"لم يتم تحقق من الحساب"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return Response({
            "id":user.id, 
             "email":email, 
            "Token":token.key, 
       
                         },status=status.HTTP_202_ACCEPTED)
         
@api_view(['POST'])
@permission_classes([AllowAny])
def Reset_password(req):
    email=req.query_params.get("email")
    if not email:
        return Response({"Erorr":"البريد المدخل غير معرف"},status=status.HTTP_404_NOT_FOUND) 
    code=req.data.get("code")   
    if not code:
        return Response({"Erorr":"الرمز غير معرف"},status=status.HTTP_404_NOT_FOUND)
    user=User.objects.filter(email=email).first()
    if not user:
        return Response({"Erorr":"البريد المدخل غير موجود"},status=status.HTTP_400_BAD_REQUEST)
    profile=user.profile
    if profile.Email_code != code:
        return Response({"Erorr":"الرمز المدخل خاطئ"},status=status.HTTP_400_BAD_REQUEST)
    profile.Activ=True
    profile.Email_code=None
    profile.save()
    token,created =Token.objects.get_or_create(user=user)
    
    return Response({
            "id":user.id,
             "email":email,
            "Token":token.key,
    },status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
@permission_classes([AllowAny])
def For_get_password_st1(req):
   code=str(random.randint(100000,999999))
   email=req.data.get("email")   
   if not email:
    return Response({"Error": "البريد غير معرف"},status=status.HTTP_404_NOT_FOUND)
   user=User.objects.filter(email=email).first()
   if not user:
       return Response({"البريد الالكتروني المدخل خاطئ"},status=status.HTTP_400_BAD_REQUEST)
   profile=user.profile
   profile.Email_code=code
   profile.save()
   html_contex=f"""
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>Verification Code</title>
</head>
<body style="margin:0; padding:0; background-color:#57595B; font-family:Arial, sans-serif; color:#fff;">
    <!-- رأس الرسالة -->
    <table width="100%" cellspacing="0" cellpadding="0" style="background-color:#2b2b2c; height:80px;">
        <tr>
            <td align="center">
                <table width="600" cellspacing="0" cellpadding="0">
                    <tr>
                        <td align="left" style="padding-left:10px; color:#ffffff; font-weight:bold; font-size:20px;">
                            Computer Academic
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>

    <!-- محتوى الرسالة -->
    <table width="100%" cellspacing="0" cellpadding="0">
        <tr>
            <td align="center" style="padding:40px 0;">
                <table width="600" cellspacing="0" cellpadding="0" style="background-color:#0F172A; border-radius:10px; padding:30px;">
                    <tr>
                        <td align="center">
                            <h1 style="color:gold; margin-bottom:20px;">مرحبا {user.profile.Name}</h1>
                            <p style="text-align:center; margin-bottom:20px;">
                                   :( حزينين لسماع اخبار نسيانك لرمز سري Computer Academic كادر
                            </p>
                            <p style="text-align:center; margin-bottom:30px;">
                           لكن لا عليك كل ما تحتاجه هو ان تسجل رمز الموجود<br>
                              :) تحت لكي تستطيع انشاء رمز جديد و استكمال تصفحك بداخل منصتنا 
                            </p>
                            <h2 style="background-color:#333; color:#fff; padding:20px; border-radius:10px; display:inline-block; font-size:24px;">
                                {code}
                            </h2>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
        """
   resend.api_key = settings.RESEND_API_KEY

   resend.Emails.send({
        "from": "Computer Academic <codeprogram2003@gmail.com>",
        "to": [user.email],
        "subject": "اعادة تعيين كلمة السر",
        "html": html_contex
    })
   return Response({"تم ارسال رمز سري الى بريد الالكتروني"},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def For_get_password_st2(req):
    code=req.data.get("code")
    email=req.data.get("email")
    user=User.objects.filter(email=email).first()
    profile=user.profile
    if profile.Email_code !=code:
        return Response({"الرمز مدخل خاطئ"},status=status.HTTP_400_BAD_REQUEST)
    profile.Email_code=None
    profile.save()
    return Response({"تم تحقق من الرمز الان يمكنك تغير رمز سري"},status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([AllowAny])
def For_get_password_st3(req):   
    email=req.data.get("email")
    Password=req.data.get("password")
    Confirm_password=req.data.get("Confirm_password")
    user=User.objects.filter(email=email).first()
    if Password !=Confirm_password:
        return Response({" كلمة مرور غير مطابقه"},status=status.HTTP_400_BAD_REQUEST)
    user.set_password(Password)
    user.save()
    token,create=Token.objects.get_or_create(user=user)
    return Response({
            "id":user.id,
             "email":email,
            "Token":token.key,
       
                         },status=status.HTTP_202_ACCEPTED)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def Updit_Profile(req):
    user=req.user
    profile=user.profile
    Name=req.data.get("Name")
    Profile_image=req.FILES.get("Profile_image")
    Bio=req.data.get("Bio")
    password=req.data.get("password")
    Change_password=req.data.get("Change_password")
    Confirm_password=req.data.get("Confirm_password")
    if Name:
        profile.Name=Name
        profile.save()
    if Profile_image:
        profile.Profile_image=Profile_image
        profile.save() 
    if Bio:
        profile.Bio=Bio
        profile.save() 
    if password:
        if not user.check_password(password):
            return Response({'erorr':"the Password is wrong"},status=status.HTTP_400_BAD_REQUEST)
        if Change_password !=Confirm_password:
            return Response({"erorr":"Password not matched"},status=status.HTTP_400_BAD_REQUEST)
        user.set_password(Change_password)
        user.save()
    token,create=Token.objects.get_or_create(user=user)
    return Response({"Mesage":"تم تحديث المعلومات","data":{
        "id":user.id,
        "Name": profile.Name,
        "Profile_image":req.build_absolute_uri(user.profile.Profile_image.url),
        "Bio":user.profile.Bio,
        "email":user.email,
        "Verified":profile.Verified,
        "token":token.key
        
        
    }}) 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Profile_user(req,id):
    user=req.user 
    profile=Profile.objects.filter(user__id=id).first()
    if not profile:
        return Response({"erorr":"There is no profile for this user."},status=status.HTTP_404_NOT_FOUND)
    summary_bank=Summary_Bank.objects.filter(user__id=id,Publish=True)
    data_summary=[]
    
    for Data_summary in summary_bank:
        data_summary.append({
            "id":Data_summary.id,
            "File_name":Data_summary.File_name,
            "File":Data_summary.File.url,
            "Level":Data_summary.Level,
            "Course":Data_summary.Course,
            "Departments":[d.Short_code_department for d in Data_summary.Departments.all()],
            
        })
    
    return Response({
            "Profile":{
                "id":profile.id,
                "Name":profile.Name,
                "Profile_image":profile.Profile_image.url,
                "Bio":profile.Bio,
                "Verified":profile.Verified,
                "StarPont":summary_bank.count() * 3,
                },
            "data_summary":data_summary
        })
    
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserSetting(req):
   user=req.user  
   profile=Profile.objects.filter(user=user).first()
   if not profile:
       return Response({
           "erorr":"the user dont have a Token"
       })
       
   else:
       
         return Response({
               "Profile":{
                "id":profile.id,
                "Name":profile.Name,
                "Profile_image":req.build_absolute_uri(user.profile.Profile_image.url),
                "Bio":profile.Bio
                }
       })

