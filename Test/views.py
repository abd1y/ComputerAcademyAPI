from django.shortcuts import render,get_object_or_404
from .models import Test
from rest_framework.decorators import api_view
from rest_framework.response import Response   
from .serializers import TestSerializer 
# Create your views here.
@api_view(['GET'])
def test_view(request):
    data=Test.objects.all()
    ser=TestSerializer(data,many=True)
    return Response(ser.data)


@api_view(['POST'])
def create_test(request):
    ser=TestSerializer(data=request.data)
   
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    else:
        return Response(ser.errors)
    

@api_view(['PUT'])
def update_test(request, pk):
    data=get_object_or_404(Test, pk=pk) 
    ser=TestSerializer(instance=data,data=request.data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    else:
        return Response(ser.errors)  















@api_view(['DELETE'])
def delete_test(request, pk):
   data=get_object_or_404(Test, pk=pk) 
   data.delete()
   return Response(status=204)

@api_view(['GET'])
def search(request,id):
    data=get_object_or_404(Test,id=id)
    ser=TestSerializer(data)
    return Response(ser.data)

