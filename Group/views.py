from django.shortcuts import render
from rest_framework.response import Response
from .models import Group,Member,Post,Comment
from .serializers import PostSer
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework import status
# Groups
@api_view(['Post'])
@permission_classes([IsAuthenticated])
def Creat_Groups(req):
    user=req.user
    data_group=req.data
    Level=req.data.get("Level")
    group_name= req.data['group_name']
    print (len(group_name))
    if len(group_name)<3:
        return Response({"erorr":"Group name must be at least 3 characters long."},status=status.HTTP_400_BAD_REQUEST)
    if  Level not in ['1','2','3','4']:
        return Response({"error":"Level must be between 1 and 4"},status=status.HTTP_400_BAD_REQUEST)
    if not data_group:
        return Response({"mesg":"The entered data is incorrect."},status=status.HTTP_400_BAD_REQUEST)
    group=Group.objects.create(
        group_name=group_name,
        Level=Level,
        owner=user
    )
    member=Member.objects.create(
        user=user,
        group=group,
        role="Admin"
    )
    group.save()
    member.save()
    return Response({
        "mesg":"The group was successfully created",
        "data":{
            "id_group":group.id,
            "group_name":group.group_name,
            "Level":group.Level,
            " Group_code":group. Group_code,
            "owner":group.owner.first_name,
            "allow_post":group.allow_post,
            "allow_comments":group.allow_comments
        }
    })

@api_view(['Post'])
@permission_classes([IsAuthenticated])
def Search_Groups(req):
       user=req.user
       Search=req.data['Search']
       Groups_code=Group.objects.filter(Group_code=Search).first()
       if not Search.startswith("#"):
         return Response({"error":"The code must begin with #"},status=status.HTTP_400_BAD_REQUEST)  
       if not Groups_code:
           return Response({"Mesg":"con't found any Group"},status=status.HTTP_400_BAD_REQUEST)
       member=Member.objects.filter(user=user,group=Groups_code).exists()
       if member:
           isMember=True
       else:
           isMember=False
       return Response({
        "data":{
            "id_group":Groups_code.id,
            "group_name":Groups_code.group_name,
            "Level":Groups_code.Level,
            "Group_code":Groups_code. Group_code,
            "owner":Groups_code.owner.first_name,
            "allow_post":Groups_code.allow_post,
            "allow_comments":Groups_code.allow_comments,
            "isMember":isMember
        }
    })
       
@api_view(['PUT'])
@permission_classes([IsAuthenticated])      
def Upsit_data_Groups(req):
    user=req.user
    allow_post = req.data.get('allow_post')
    allow_comments = req.data.get('allow_comments')
    group_name = req.data.get('group_name')
    Group_code = req.data.get('Group_code')
    
    Groups=Group.objects.filter(Group_code=Group_code).first()
    if not Groups:
        return Response({"erorr":"The Group was not found"},status=status.HTTP_400_BAD_REQUEST)
    if Groups.owner != user:
        return Response({"erorr":"Only owner can Undit data"})
    if  group_name is not None:
            if len(group_name)<3:
             return Response({"erorr":"Group name must be at least 3 characters long."},status=status.HTTP_400_BAD_REQUEST)
            Groups.group_name=group_name
    if allow_post is not None:
        print(allow_post)
        Groups.allow_post=allow_post
    if  allow_comments is not None:
         Groups.allow_comments=allow_comments    
    Groups.save()
    return Response({"data":{
        "id_group":user.id,
        "group_name":Groups.group_name,
        "Level":Groups.Level,
        "allow_post":Groups.allow_post,
        "allow_comments":Groups.allow_comments,
    }})


#  Member Groups
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Member_group(req):
    Group_code = req.query_params.get('Group_code')
    groups=Group.objects.filter(Group_code=Group_code).first()
    if not groups:
        return Response({"erorr":"cont find the Groups"},status=status.HTTP_404_NOT_FOUND)
    members=Member.objects.filter(group=groups)
    member_data=[]
   
    for m in members:
    
       data={
           "id":m.user.id,
            "Name":m.user.profile.Name,
            "Profile_image":m.user.profile.Profile_image.url,
            "role":m.role
        }
       member_data.append(data)
    return Response({
        "data":{
            "id_Group":groups.id,
            "group_name":groups.group_name,
            "Level":groups.Level,
                  "allow_post":groups.allow_post,
        "allow_comments":groups.allow_comments,
            "Member":member_data
        }
    })
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Join_Leave_group(req):
    user=req.user
    Group_code=req.data.get("Group_code")
    group=Group.objects.filter(Group_code=Group_code).first()
    if not group:
        return Response({"erorr":"cont find the Group"})
    member=Member.objects.filter(user=user,group=group).first()
    if member:
        isMember=False
        member.delete()
        return Response({"Mesg":"Exit from the group it's successfully "})
    Member.objects.create(
        user=user,
        group=group,
        role="Member",
       
    )
    isMember=True
    return Response({"Mesg":"Joined the group it's successfully"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def Leave_groups(req):
     user=req.user
     Group_code=req.query_params.get("Group_code")
     group=Group.objects.filter(Group_code=Group_code).first()
     if not group:
        return Response({"erorr":"cont find the Group"})
     member=Member.objects.filter(user=user,group=group).first()
     if member:
        isMember=False
        member.delete()
        return Response("Delete is done")
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_group(req):
    user=req.user 
    Group_code=req.query_params.get("Group_code")
    group=Group.objects.filter(owner__id=user.id,Group_code=Group_code).first()
    if not group:
        return Response({'erorr':"con't delete the Groups"})
    else:
        group.delete()
        return Response("The group was successfully deleted")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def My_Groups(req):
   user=req.user  
   member=Member.objects.filter(user=user).order_by("-created_at")
   data=[]
   for m in member:
       data.append({
           "Group_id":m.group.id,
           "group_name":m.group.group_name,
           "owner":m.group.owner.first_name,
           "Level":m.group.Level,
           "Group_code":m.group.Group_code
       })  
       
   return Response({"Group":data})

# Post
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Show_post_Group(req):
    user=req.user
    code=req.query_params.get("Group_code")
    group=Group.objects.filter(Group_code=code).first()
    if not group:
        return Response({"erorr":"The group was not found"},status=status.HTTP_404_NOT_FOUND)
    members=Member.objects.filter(user=user, group=group).first()
    if not members:
        return Response({"erorr":"You are not a member of a group"},status=status.HTTP_404_NOT_FOUND)
    posts=Post.objects.filter(member__group=group).order_by('-id')

    serPost=PostSer(posts,many=True,context={'request': req})
    return Response({
        "data":{
            "id_group":group.id,
            "group_name":group.group_name,
            "posts":serPost.data
        }
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Post_Group(req):
    user=req.user
    code=req.query_params.get("Group_code")
    group=Group.objects.filter(Group_code=code).first()
    if not group:
          return Response({"erorr":"The group was not found"},status=status.HTTP_404_NOT_FOUND)
    member=Member.objects.filter(user=user,group=group).first()
    if not member:
          return Response({"erorr":"cann't post because you are not a member of a group."},status=status.HTTP_404_NOT_FOUND)
    title=req.data.get('title')
    if not title or title.strip() == "":
     return Response({"error": "title is required"}, status=400)
    post=Post.objects.create(
        member=member,
        title=title,
           media=req.data.get('media', None),
        
    )
    post.save()
    
    return Response({"Mesg":"Post created successfully","post_id":post.id})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def Edit_Post(req,post_id):
    user=req.user
    code=req.query_params.get("Group_code")
    group=Group.objects.filter(Group_code=code).first()
    if not group:
          return Response({"erorr":"The group was not found"},status=status.HTTP_404_NOT_FOUND)
    member=Member.objects.filter(user=user,group=group).first()
    if not member:
          return Response({"erorr":"cann't post because you are not a member of a group."},status=status.HTTP_404_NOT_FOUND)
    post=Post.objects.filter(id=post_id).first() 
    if not Post:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    if "title" in req.data:
        post.title = req.data.get("title")
    if "media" in req.data:
        post.media = req.data.get("media")
    post.save()
    
    return Response({"mesg":"Post successfully edited"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def Delet_Post(req,post_id):
    user=req.user
    code=req.query_params.get("Group_code")
    group=Group.objects.filter(Group_code=code).first()
    if not group:
          return Response({"erorr":"The group was not found"},status=status.HTTP_403_FORBIDDEN)
    member=Member.objects.filter(user=user,group=group).first()
    if not member:
          return Response({"erorr":"cann't post because you are not a member of a group."},status=status.HTTP_403_FORBIDDEN)
    post=Post.objects.filter(id=post_id).first() 
    if not post:
        return Response({"error": "Post not found"}, status=status.HTTP_403_FORBIDDEN) 
    if member.role == "Admin" or post.member == member:
     post.delete()
    else:
        return Response({"Erorr":"The post cannot be deleted because you did not post it or you are not the admin."})
    return Response({"Mesg":"The delete is successfully"})   

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Toggle_Like(req,post_id):
    user=req.user
    post=Post.objects.filter(id=post_id).first()
    if not post:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    if user in post.by_like.all():
        post.by_like.remove(user)
        post.Like=post.by_like.count()
        action="unlike"
    else:
        post.by_like.add(user)
        post.Like=post.by_like.count()
        action="liked"
    post.save()
    is_liked = user in post.by_like.all()
    serializer = PostSer(post, context={'request': req})
    return Response({'msg':f"Post {action}","like":post.Like,"is_liked":is_liked})

# Comments
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(req,post_id):
    user=req.user
    code=req.query_params.get("Group_code")
    group=Group.objects.filter(Group_code=code).first()
    if not group:
          return Response({"erorr":"The group was not found"},status=status.HTTP_403_FORBIDDEN)
    member=Member.objects.filter(user=user,group=group).first()
    if not member:
        return Response({"erorr":"You are not a member of a group"},status=status.HTTP_403_FORBIDDEN)
    post=Post.objects.filter(id=post_id).first()
    if not post:
        return Response({"erorr":"The post is not available."},status=status.HTTP_404_NOT_FOUND)
    comment=Comment.objects.create(
        post=post,
        member=member,
        content=req.data.get("content")
    )
    comment.save()
    return Response({
        "Msg":"A comment was successfully added.",
        "comment_id":comment.id,
        "content":comment.content,
        "user_id":member.user.id,
        "member_name":member.user.profile.Name,
        "Profile_image":req.build_absolute_uri(member.user.profile.Profile_image.url),
    })
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(req,comment_id):
       user = req.user
       comment=Comment.objects.filter(id=comment_id).first()
       if not comment:
           return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
       
       if comment.member.user == user or comment.member.role=="Admin":
        comment.delete()
        return  Response({"Msg":"The comment was successfully deleted"})
       else:
        return Response({"error":"A comment cannot be deleted because you are neither the commenter nor an admin."},status=status.HTTP_403_FORBIDDEN)
