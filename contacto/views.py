from http import HTTPStatus
from rest_framework import serializers
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
#llamamos a utilidades para usar 
from utilidades import utiles
#swaggegr
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

#para que swagger sepa que campos esperar 

class ContactoSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    correo = serializers.EmailField()
    telefono = serializers.CharField()
    mensaje = serializers.CharField()



class Clase1(APIView):
    """configuracion para el swagger informacion del endpoint"""
    @swagger_auto_schema(
        operation_description="Endpoint para contactos",
        responses={
            200:"Success",
            400: "Bad Request",
            500: "Internal Server Error"
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description="Nombre"),
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description="Email"),
                'telefono': openapi.Schema(type=openapi.TYPE_STRING, description="telefono"),
                'mensaje': openapi.Schema(type=openapi.TYPE_STRING, description="mensaje"),
            },
            # se usa para indicar que Campos son obligatorios
            required=['nombre', 'correo', 'telefono', 'mensaje'] 
        )
    )
    def post(self, request):
        """esto es un deserializador que recibe los datos del contacto de parte dedl cliente"""
        serializer = ContactoSerializer(data=request.data)
        """si los datos no son validos se arroja un mensaje de errror"""
        if not serializer.is_valid():
            return Response({"estado": "error", "mensaje": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"estado": "ok", "mensaje": "el mensaje fue enviado correctamente"}, status=status.HTTP_200_OK)
        
        """validaciones de cada campo de contacto"""
        if not request.data.get("nombre"):
            return Response({"estado":"error", "mensaje":"el campo nombre no puesde estar vacio"},
                                status= HTTPStatus.BAD_REQUEST)
        #validacion para que el campo correo no este vacio
        if not request.data.get("correo"):
            return Response({"estado":"error", "mensaje":"el campo correo no puesde estar vacio"},
                                status= HTTPStatus.BAD_REQUEST)
        #validacion para que el campo telefono no este vacio
        if not request.data.get("telefono"):
            return Response({"estado":"error", "mensaje":"el campo telefono no puesde estar vacio"},
                                status= HTTPStatus.BAD_REQUEST)
        #validacion para que el campo mensaje no este vacio
        if not request.data.get("mensaje"):
            return Response({"estado":"error", "mensaje":"el campo mensaje no puesde estar vacio"},
                                status= HTTPStatus.BAD_REQUEST)
        """graba los datos en la base de datos en caso que no haya errores"""
        try:
            Contacto.objects.create(
                nombre = request.data['nombre'],
                correo = request.data['correo'],
                telefono = request.data['telefono'],
                mensaje = request.data['mensaje'])
            
            #la fecha no se coloca porque se guarda automaticamente al crear el objeto
            # Contacto.objects.create, hay que tener en cuenta que ya se esta guardando la fecha.
            html = f"""
            <html>
                <head>
                    <title>Mensaje de contacto</title>
                </head>
                <body>
                    <h1>Mensaje de contacto</h1>
                    <p>Nombre: {request.data['nombre']}</p>
                    <p>Correo: {request.data['correo']}</p>
                    <p>Telefono: {request.data['telefono']}</p>
                    <p>Mensaje: {request.data['mensaje']}</p>
                </body>
            """ 
            utiles.sendMail(html, "Mensaje de prueba y confirmacion", request.data['correo'])
        except Exception as e:
            #el format se usa para formatear el mensaje de error
            return Response({"estado":"error", "mensaje":"ocurrio un error al guardar el mensaje: {}".format(str(e))}, 
                            status=HTTPStatus.BAD_REQUEST)
            
            
        
        #este return identado a la altura del try con la creacion de los daros
        return Response({"estado":"ok", "mensaje":"el mensaje fue enviado correctamente"},
                                status= HTTPStatus.OK)
        
        #Nota: la fecha configurada en el settings.py no afecta a la fecha que se guarda en la base de datos,
        #ya que esta se guarda automaticamente al crear el objeto, por lo que no es necesario configurarla
        #"sin embargo hay que etener en cuanta que esta trabaja con el horario que hayamos configurado en el servidor
        #por lo que si el servidor esta en otro horario, la fecha que se guarda sera la del servidor y no la del cliente"
        
        
        
        
        
        
        
        
            
            
            
