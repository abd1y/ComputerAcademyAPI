from django.urls import  path
from . import views
urlpatterns = [
    path("get_docement/",views.Get_All_docement),
    path("Post_docement/",views.Post_docement),
    path("Filter_docement/",views.Filter_docement),
]