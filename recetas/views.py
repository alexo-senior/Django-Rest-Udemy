from django.shortcuts import render
from http import HTTPStatus
from django.http import JsonResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response  # Importa Response
from .serializers import RecetaSerializer
from .models import *
from rest_framework import status #import status
from django.utils.dateformat import DateFormat
import os
from dotenv import load_dotenv




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
            
            
            
#CONSULTAR RECETA POR ID            
        
class Clase2(APIView):
    def get(self, request, id):
        try:
            #consulta los objetos receta por id
            data = Receta.objects.filter(id=id).get()
            
            if not data:
            #si no hay datos devuelve un 204 no content
                return Response(status=status.HTTP_204_NO_CONTENT)
            #formateo de todos los datos de la receta, entonces por medio del id se obtiene la receta 
            return Response({"data":{"id":data.id, "nombre":data.nombre, "slug":data.slug, "tiempo":data.tiempo,
                                    "descripcion":data.descripcion, "fecha":DateFormat(data.fecha).format("d/m/Y"),
                                    "categoria_id":data.categoria_id, "imagen":f"{os.getenv('BASE_URL')}uploads/recetas/{data.foto}"}}, 
                            status=status.HTTP_200_OK)
                                    
                                    
            #return Response({"data": datos_json.data}, status=status.HTTP_200_OK)
        except Receta.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #maneja la excepcion en caso de error de servidor
        except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        
            
        
        
        
            
        
            
            
            
            
    
    
    
    
    