from django.contrib import admin
from .models import Summary_Bank,Departments_gategory
# Register your models here.

class Summary_bank_Admin(admin.ModelAdmin):
    list_display=("File_name",'user__Name','user__Verified',"Publish")
    search_fields=("File_name",)
admin.site.register(Summary_Bank,Summary_bank_Admin)

admin.site.register(Departments_gategory)