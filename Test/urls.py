from django.urls import  path
from . import views
urlpatterns = [
    path('Test/', views.test_view),
    path('Test/create', views.create_test),
    path('Test/update/<int:pk>', views.update_test),
    path('Test/delete/<int:pk>', views.delete_test),
    path('Test/search/<int:id>', views.search),
]
