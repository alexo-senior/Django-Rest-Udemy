from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, Http404
from .models import *
#para hacer las validaciones de los campos de la clase 1
#a apesar que el modelo esta importado User es aparte de django 
from django.contrib.auth.models import User

#valida los correos ya creados en la base de datos, no crea nuevos usuarios
#para crear nuevos usuarios es otro endpoint
class Clase1( APIView):
    def post(self, request):
        #si la rrequest.data es igual a none o no existe deb¿vuelve un mensaje de error 
        #la misma sentencia de codigo prra validar los demas campos 
        if request.data.get("nombre") == None or not request.data.get("nombre"):
            return Response({"error":"el campo nombre es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("correo") == None or not request.data.get("correo"):
            return Response({"error":"el campo correo es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("pasword") == None or not request.data.get("pasword"):
            return Response({"error":"el campo pasword es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        #validar el correo, busca el usuario por correo
        try:
            usuario = User.objects.get(email=request.data["correo"])
        except User.DoesNotExist:
                return Response({
                    "estado": "error", 
                    "mensaje":"El correo no existe o no esta disponible" },
                        status=status.HTTP_400_BAD_REQUEST)
            
                
            
        #validar el pasword con check_password
        if usuario.check_password(request.data["pasword"]): 
            return Response({"estado":"ok", "mensaje":"el pasword es correcto"},
                        status=status.HTTP_200_OK)
        else:
            return Response({"estado": "error", "mensaje":"contraseña incorrecta"},
                        status=status.HTTP_400_BAD_REQUEST)
        
        

        
        
        
        
        
            
            
    
        
