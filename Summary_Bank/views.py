from django.shortcuts import render
from rest_framework.response import Response
# Create your views here.
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework import status
from .models import Summary_Bank,Departments_gategory
from .serializers import Sumary_bank_Serilazer
from .pagnation import MyPagination
from authentication.models import Profile

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def Get_All_docement(req):
    sumaryBank=Summary_Bank.objects.filter(Publish=True).order_by('-id')
    pagnator=MyPagination()
    page=pagnator.paginate_queryset(sumaryBank,req)
    Ser=Sumary_bank_Serilazer(page,many=True)
    return pagnator.get_paginated_response({"data":Ser.data})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def Post_docement(req):
    user=req.user 
    file_name=req.data.get('File_name')
    fileObj=req.FILES.get('File')
    Level=req.data.get('Level')
    Course=req.data.get('Course')
    code=req.data.getlist('Departments')
    profile=Profile.objects.filter(user=user).first()
    if not profile:
        return Response({"erorr":"You do not have permission to publish a summary"},status=status.HTTP_403_FORBIDDEN)
    erorrMsg={}
    if not file_name:
        erorrMsg['File_name']=' The Field Docement Name is required'
    if not fileObj:
        erorrMsg['File']='Please upload a PDF file.'
    if not code:
     erorrMsg['Departments'] = 'You must select at least one department.'
    if erorrMsg:
        return Response(erorrMsg,status=status.HTTP_400_BAD_REQUEST)
    summary_bank=Summary_Bank.objects.create(
        user=profile,
        File_name=file_name,
        File=fileObj,
        Level=Level,
        Course=Course,
    )
 
 
    departments=Departments_gategory.objects.filter(
        Short_code_department__in=code
    )
    summary_bank.Departments.set(departments)
  
    summary_bank.save()
    return Response({"Msg":"The summary has been successfully published; please await approval."},status=status.HTTP_201_CREATED)
@api_view(["POST"])
@permission_classes([IsAuthenticated])    
def Filter_docement(req):
    qs=Summary_Bank.objects.filter(Publish=True)
    Departments=req.data.get("Departments",[])
    Level=req.data.get("Level",[])  
    Course=req.data.get("Course",[])
    
    if Departments:
        qs=qs.filter(Departments__Short_code_department__in=Departments)
    if Level:
        qs=qs.filter(Level__in=Level)
    if Course:
        qs=qs.filter(Course__in=Course)
    qs = qs.order_by('-id') 
    Ser=Sumary_bank_Serilazer(qs,many=True)
    return Response({'data':Ser.data})