


from django.urls import  path
from .views import SingIn,Longin,Reset_password,For_get_password_st1,For_get_password_st2,For_get_password_st3,Updit_Profile,Profile_user,UserSetting


urlpatterns = [

    path('signup/',SingIn,name='signup'),
    path('LongIn/',Longin,name='LongIn'),
    path("Reset-password/",Reset_password,name="Reset_password"),
    path("For-get-password_Step1/",For_get_password_st1,name="send_resent_password"),
    path("For-get-password_Step2/",For_get_password_st2,name='For_get_password_st2'),
    path("For-get-password_Step3/",For_get_password_st3,name='For_get_password_st2'),
    path("Updit-profile/",Updit_Profile,name="Updit_Profile"),
    path("UserSetting/",UserSetting),
    path("Profile_user/<int:id>/",Profile_user,name="Updit_Profile"),
    

    
]
