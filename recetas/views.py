from django.shortcuts import render
from http import HTTPStatus
from django.http import JsonResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response  # Importa Response
from .serializers import RecetaSerializer
from .models import *
from rest_framework import status #import status

# Create your views here.
"""class Clase1(APIView):
    def get(self, request):
        #se obtiene el id de la receta desde el ultimo id de la base de datos
        #se ordena de forma descendente para obtener el ultimo id
        data = Receta.objects.order_by('-id').all()
        #se crea una variable que contiene el serializador de recetasserializer
        datos_json = RecetaSerializer(data, many=True)
        #se retorna un json con el contenido de la variable datos_json
        #el metodo data convierte el objeto en un diccionario de python
        return JsonResponse({"data": datos_json.data})"""
        
class Clase1(APIView):
    def get(self, request):
        try:
            """consulta los objetos receta ordenados de forma descendente por id"""
            data = Receta.objects.order_by('-id').all()

            if not data:
                return Response(status=status.HTTP_204_NO_CONTENT)  # Devuelve 204 si no hay datos

            datos_json = RecetaSerializer(data, many=True)
            return Response({"data": datos_json.data}, status=status.HTTP_200_OK)  # Devuelve 200 OK
        except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
            
            
            
    
    
    
    
    