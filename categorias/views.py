from django.shortcuts import render
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.response import Response
from . models import Categoria



#se crea la clase Clase1 que hereda de APIView. 
class Clase1(APIView):
    def get(self, request):
        #se crea la variable data que contiene todos los datos de la tabla Categoria
        #para eso se debe importar primero la tabla Categoria
        #luego se usa el metodo objects.order_by('-id').all() para que los datos se ordenen por id de forma descendente
        data = Categoria.objects.order_by('-id').all()
        #se puede hacer una respuesta tipo response para probar que los datos se estan mostrando correctamente
        return Response(data)
        pass
    
    
        
        
        
    
    
    
