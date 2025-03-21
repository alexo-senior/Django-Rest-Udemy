from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse

#se crea la clase Clase1 que hereda de APIView. 
class Clase1(APIView):
    def get(self, request):
        pass
    
    
