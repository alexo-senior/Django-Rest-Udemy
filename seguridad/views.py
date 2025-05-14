from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, Http404
from .models import *
import uuid
import os 
from dotenv import load_dotenv

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
        if request.data.get("password") is None or not request.data.get("password"):
            print("DEBUG: Password field is missing or empty:", request.data.get("password"))
            return Response({"error":"el campo password es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        #validar el correo, busca el usuario por correo
        
        if User.objects.filter(email=request.data['correo']).exists():
            return Response({"estado": "error", 
                            "mensaje": f"el correo {request.data['correo']} no existe o no esta disponible"}, 
                            status=status.HTTP_400_BAD_REQUEST)
    
            
        #se crea el token con uuid y la url que va a usar el usuario para verficar su cuenta
        
        token = uuid.uuid4()
        url = f"{os.getenv('BASE_URL')}/api/v1/seguridad/verificacion/{token}"
        print(url)
        try:
            #se crea primero el usuario en la base de datos
            u = User.objects.create_user(
                #se usa tambien el correo como username
                username=request.data['correo'],
                email=request.data['correo'],
                password=request.data['password'], 
                first_name=request.data['nombre'],
                last_name="",#lo podemos dejar vacio para la prueba
                is_active=0
            )
            #registro en cascada por la informacion del modelo User
            #se crea el token para el usuario
            UsersMetadata.objects.create(token=token, user_id=u.id)
        except Exception as e:
            return Response({"estado": "error", 
                            "mensaje": f"ocurrio un error inesperado en la creacion del usuario: {str(e)}"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        #se hace el return de la respuesta exitosa
        return Response({"estado": "ok", 
                        "mensaje": "se crea el registro de usuario exitosamente"}, 
                        status=status.HTTP_201_CREATED)
        
        
        

        
        
        
        
        
            
            
    
        
