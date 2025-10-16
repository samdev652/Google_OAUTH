from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
def Home(request):
    return Response('Hey Gys Just written my first Django rest Api in views file')