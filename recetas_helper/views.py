from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, Http404, HttpResponseRedirect

#las recetas deben ir asociadas a un usuario, por lo que se debe crear un modelo de usuario
#es aconsejable reservar el usuario numero 1 para el administrador 
class Clase1(APIView):
    def get(self, request):
        pass
    
    