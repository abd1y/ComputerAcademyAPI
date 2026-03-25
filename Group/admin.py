from django.contrib import admin
from .models import Group,Member,Post,Comment
# Register your models here.
admin.site.register(Comment)


class GroupAdmin(admin.ModelAdmin):
    search_fields= ("group_name",)   
admin.site.register(Group,GroupAdmin)

class MemberAdmin(admin.ModelAdmin):
    list_display=("get_Name_Member","get_role_display","get_group_name")
    search_fields=("user__first_name","group__group_name")
    def get_Name_Member(self,obj):
        return obj.user.first_name
    get_Name_Member.short_description ="Member Name"
    
    
    def get_group_name(self,obj):
        return obj.group.group_name
    get_group_name.short_description="Group Name"
admin.site.register(Member,MemberAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display=("get_Member_Post","get_Group_Post")
    search_fields=("member__group__group_name","member__user__first_name")
    
    
    def get_Member_Post(self,obj):
        return obj.member.user.first_name
    get_Member_Post.short_description="Name User"
    def get_Group_Post(self,obj):
        return obj.member.group.group_name
    get_Group_Post.short_description="Group"
admin.site.register(Post,PostAdmin)

