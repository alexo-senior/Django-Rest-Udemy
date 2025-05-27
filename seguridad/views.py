from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, Http404, HttpResponseRedirect
from .models import *
import uuid
import os 
from dotenv import load_dotenv
from utilidades import  utiles
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from jose import jwt#paara el manejo del token de seguridad
#para el manejo de la clave secreta, que viene con el settings de django
from django.conf import settings
from datetime import datetime, timedelta
import time


#para hacer las validaciones de los campos de la clase 1
#a apesar que el modelo esta importado User es aparte de django 

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
                    "mensaje": f"el correo {request.data['correo']} ya está registrado"}, 
                    status=status.HTTP_400_BAD_REQUEST)

# Si no existe, continúa con la creación del usuario...      
        #se crea el token con uuid y la url que va a usar el usuario para verficar su cuenta
        #uuid es un modulo de python para generar un uuid 4
        token = uuid.uuid4()
        #esto permite que la url se pueda usar en el entorno de desarrollo y produccion
        #se carga el archivo .env para obtener la variable de entorno BASE_URL
        url = f"{os.getenv('BASE_URL')}/api/v1/seguridad/verificacion/{token}"
        #print(url)
        try:
            #se crea primero el usuario en la base de datos
            #se crea una variable u para guardar el usuario creado
            #se usa create_user no create, ya que create_user hace el hash de la contraseña
            #de forma automatica
            #se sigue usando create para los demas metodos este es solo para el user
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
            html=f"""
            <h3>Verificacion de la cuenta de Alexis</h3>
            Hola {request.data["nombre"]} te has registrado en la aplicacion de Alexis
            <p>Para verificar tu cuenta, por favor haz click en el siguiente enlace:</p>
            <a href="{url}">{url} Verificar su cuenta</a>
            <br>
            o copia y pega la siguiente url en tu navegador:</p>
            <a href="{url}</a>
            <br>
            <p>Si no solicitaste esta verificacion, puedes ignorar este mensaje</p>
            """
            utiles.sendMail(html, "verificacion de cuenta", request.data["correo"])
            
        except Exception as e:
            return Response({"estado": "error", 
                            "mensaje": f"ocurrio un error inesperado en la creacion del usuario: {str(e)}"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        #se hace el return de la respuesta exitosa
        return Response({"estado": "ok", 
                        "mensaje": "se crea el registro de usuario exitosamente"}, 
                        status=status.HTTP_201_CREATED)
        
        
        
from django.http import HttpResponseRedirect
import os

class Clase2(APIView):
    def get(self, request, token):
        if token is None or not token:
            return Response({"estado": "error",
                            "mensaje": "El token es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # data2 contiene el objeto UsersMetadata si se encuentra el token o es igua al que me viene en la url
            #y por medio de un nuevo filter ir a la tabla User y preguntar si 
            #el  campo is_active es igual a 0 , en filter() doble gion bajo a user__is_active
            data2 = UsersMetadata.objects.filter(token=token).filter(user__is_active=0).get()
            # si no se encuentra el token se devuelve un error 
            # Si el token se encuentra, obtenemos el usuario asociado
            user = User.objects.get(id=data2.user_id)
            # Activamos al usuario, que es 1 por defecto
            # pero si el usuario ya está activo, no hace nada
            if user.is_active:
                return Response({"estado": "ok",
                                "mensaje": "El usuario ya está activo"},
                                status=status.HTTP_200_OK)
            # Si el usuario no está activo, lo activamos
            user.is_active = True
            user.save()
            # Redirigir al login después de la verificación
            return HttpResponseRedirect(os.getenv("BASE_URL_FRONTEND"))
        except UsersMetadata.DoesNotExist:
            return Response({"estado": "error",
                            "mensaje": "el token no existe o ya fue utilizado"},
                            status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"estado": "error",
                            "mensaje": "Usuario asociado al token no encontrado"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"estado": "error",
                            "mensaje": f"Ocurrió un error inesperado durante la verificación: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
        
    # OTRA FORMA DE HACERLO
    # Si quieres usar esta versión alternativa, descomenta y usa como una función aparte, no como clase anidada.
    # def otra_forma_verificar_usuario(request, token):
    #     if token is None or not token:
    #         return Response({"estado": "error", 
    #                         "mensaje": "El token es requerido"}, status=status.HTTP_400_BAD_REQUEST)
    #     try:
    #         data = UsersMetadata.objects.filter(token=token).get()
    #         UsersMetadata.objects.filter(token=token).update(token="")
    #         User.objects.filter(id=data.user_id).update(is_active=1)
    #         return Response({"estado": "ok", 
    #                         "mensaje": "el usuario se activo exitosamente"}, 
    #                         status=status.HTTP_200_OK)
    #         # return HttpResponseRedirect(os.getenv('BASE_URL_FRONTED'))
    #     except UsersMetadata.DoesNotExist:
    #         return Response({"estado": "error",
    #                         "mensaje": "el token no existe"},
    #                         status=status.HTTP_400_BAD_REQUEST)
    
    
    #VALIDACION DE CREDEENCIALES DE CORREO 
    #es decir a traves de un correo y un password ya registrado en la bd
    #y poder loguear a un usuario ya creado en la base de datos 
class Clase3(APIView):
    #ESTA VEZ SERA POST
    def post(self, request):
        if request.data.get("correo") == None or not request.data.get("correo"):
            return Response({"error":"el campo correo es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("password") == None or not request.data.get("password"):
            return Response({"error":"el campo password es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        
        #para loguear al usuario
        try:
            user = User.objects.get(email=request.data["correo"])
        except User.DoesNotExist:
            return Response({"estado": "error", "mensaje": "Recurso no disponible"}, 
                            status=status.HTTP_404_NOT_FOUND)
        #PARA VALIDAR EL PASSWORD
        #auth valida el correo y el pasword ademas si el usuario esta activo
        #si el usuario esta activo y el password es correcto
        #entonces retorna un objeto de autenticacion , de lo contario
        #retorna None, o se ejecuta el bloque de else
        auth = authenticate(request, username=request.data.get("correo"), 
                        password=request.data.get("password"))
        #esto me retorna un objeto de autenticacion 
        #si el usuario no existe o el password es incorrecto 
        if auth is not None:
            #construir el token
            fecha = datetime.now()
            #generar una variable llamada: despues, que es la fecha mas un dia
            despues = fecha + timedelta(days=1)
            fecha_numero = int(datetime.timestamp(despues))
            #ahora se construye el payload
            #
            payload={"id":user.id, "ISS":os.getenv("BASE_URL"), "iat":int(time.time()), "exp":int(fecha_numero)}
            #se genera el token
            try:
                #el encode recibe el payload, la clave secreta y el algoritmo
                #en este caso es HS512 que es el algoritmo que se usa para encriptar el token
                #el payload es un diccionario que contiene la informacion del token
                #la clave secreta es la que se usa para encriptar el token
                #la clave secreta se guarda en el archivo .env y se llama SECRET_KEY
                #el algoritmo es HS512 que es el algoritmo que se usa para encriptar el token 
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS512')
                #se guarda el token en la base de datos
                #UsersMetadata.objects.filter(user_id=user.id).update(token=token)
                #se retorna el token
                #se retorna el id del usuario y el token 
                return Response({"id":user.id, "nombre":user.first_name, "token":token})
            except Exception as e:
                return Response({"estado":"error", "mensaje": "las credenciales no son validas"}, 
                            status=status.HTTP_401_UNAUTHORIZED)
            
            
            
            #return Response({"estado": "error", "mensaje": "usuario o contraseña incorrectos"})
        else:
            return Response({"estado":"error", "mensaje": "las credenciales no son validas"}, 
                        status=status.HTTP_401_UNAUTHORIZED)
            
        #AHORA COMO SE MANEJA EL TOKEN PARA LA PROTECCION DE LOS ENDPOINTS
        
        
        
        
        
            
        
        
    
        
    
        
    
        

        
        
        
        
        
            
            
    
        
