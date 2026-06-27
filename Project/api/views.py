from django.shortcuts import render
from .models import BioData
from .serializer import ProjectmodelSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import io
from rest_framework.decorators import api_view
from rest_framework import status

# from django.views.csrf import get
# Create your views here.
@api_view(['GET','PUT','PATCH'])
def singobj(request,id):
    data = BioData.objects.get(id=id)
    if request.method == 'PUT':
        parsed_data = request.data
        serializer = ProjectmodelSerializer(data, data=parsed_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"update": "success"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PATCH':
        parsed_data = request.data
        serializer=ProjectmodelSerializer(data,data=parsed_data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"update":"sucess"})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        serializer = ProjectmodelSerializer(data)   
        return Response(serializer.data)
      
@api_view(['GET','POST'])
def multiobj(request):
    if request.method == 'POST':
        parsed_data = request.data
        serializer = ProjectmodelSerializer(data=parsed_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"created":"successful"},status=status.HTTP_201_CREATED)
            
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'GET':
        data = BioData.objects.all()
        serializer = ProjectmodelSerializer(data,many=True)
        return Response(serializer.data)