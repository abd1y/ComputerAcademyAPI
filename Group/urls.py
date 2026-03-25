from django.urls import  path
from . import views
urlpatterns = [
path("creat_Groups/",views.Creat_Groups),
path("Search_Groups/",views.Search_Groups),
path("Upsit_data_Groups/",views.Upsit_data_Groups),
path("delete_group/",views.delete_group),

# Member
path("Member_Group/",views.Member_group),
path("Join_Leave_group/",views.Join_Leave_group),
path("My_Groups/",views.My_Groups),
path("Leave_groups/",views.Leave_groups),

# Post
path("show_post/",views.Show_post_Group),
path("Post_Group/",views.Post_Group),
path("Edit_post/<int:post_id>/",views.Edit_Post),
path("delete_post/<int:post_id>/",views.Delet_Post),
path("Toggle_Like/<int:post_id>/",views.Toggle_Like),

# comment
path("add_comment/<int:post_id>/",views.add_comment),
path("delete_comment/<int:comment_id>/",views.delete_comment)
]

