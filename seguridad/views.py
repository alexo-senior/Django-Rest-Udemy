from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, Http404
from .models import *


class Clase1( APIView):
    def post(self, request):
        pass
    
        
