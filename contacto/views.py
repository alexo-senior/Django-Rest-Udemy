from http import HTTPStatus
from rest_framework import serializers, generics
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.template.loader import render_to_string
#llamamos a utilidades para usar 
from utilidades import utiles
#swaggegr
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

#para que swagger sepa que campos esperar 
#es un serializador de entrada
"""
    Crea una nueva entrada de contacto, la guarda en la base de datos y
    envía un correo de confirmación al usuario.
    """
class ContactoInputSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    correo = serializers.EmailField()
    telefono = serializers.CharField()
    mensaje = serializers.CharField()

#serializador que muestra los datos del modelo    
class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = '__all__'    



class Clase1(APIView):
    """configuracion para el swagger informacion del endpoint"""
    
    @swagger_auto_schema(
        operation_description="Endpoint para crear un nuevo contacto",
        responses={
        201: openapi.Response("El contacto fue creado y el correo enviado exitosamente."),
        400: "Datos de entrada inválidos.",
        500: "Error interno del servidor."
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
        
        """esto es un deserializador que recibe los datos del contacto de parte del cliente"""
        
        serializer = ContactoInputSerializer(data=request.data)
        
        """si los datos no son validos se arroja un mensaje de errror"""
        
        if not serializer.is_valid():
            return Response({"estado": "error", "mensaje": serializer.errors}, 
                        status=status.HTTP_400_BAD_REQUEST)
            
        # Usar los datos validados por el serializador es más seguro    
        validated_data = serializer.validated_data
        
        """ 1. guarda el contacto en la base de datos"""
        try:
            # 2. Preparar y enviar el correo de confirmación
            # Es una mejor práctica usar una plantilla para el HTML del correo
            # en lugar de tenerlo directamente en la vista.
            #Contacto.objects.create(**serializer.validated_data)
            Contacto.objects.create(**validated_data)
            #envia el correo, el bloque debe estar dentro dedl try para que se ejecute
            #de forma correcta, ya que si esta fuera se detiene la ejecucion con el return
            
            html_content = render_to_string('emails/contacto_confirmacion.html',{'data':validated_data})
            
            utiles.sendMail(
                html_content, 
                "Confirmacion de tu mensaje de contacto", 
                validated_data['correo'])
            
            #paar un post que crea un recurso es mejor un codigo de estado 201 created
            return Response(
                {"estado": "ok", "mensaje": "El contacto fue creado y el correo enviado exitosamente"}, 
                        status=status.HTTP_201_CREATED)
            # Es buena idea registrar el error 'e' para futura depuración
            # # import logging
            # logger = logging.getLogger(__name__).
            # logger.error(f"Error al procesar contacto: {e}")
        except Exception as e:
            
            return Response(
                {"estado": "error", "mensaje": f"Ocurrió un error al guardar el mensaje: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        #Nota: la fecha configurada en el settings.py no afecta a la fecha que se guarda en la base de datos,
        #ya que esta se guarda automaticamente al crear el objeto, por lo que no es necesario configurarla
        #"sin embargo hay que etener en cuenta que esta trabaja con el horario que hayamos configurado en el servidor
        #por lo que si el servidor esta en otro horario, la fecha que se guarda sera la del servidor y no la del cliente"
#vista para listar los contactos
#hereda de generics.ListAPIView para simplificar el codigo        
class ContactoListView(APIView):
    """vista para listar todos los contactos.
    Usa una vista generica de DRF par un codigo mas limpio , legible y mantenible"""
    
    @swagger_auto_schema(
        operation_description="lista de todos los contactos",
        responses={
            200: openapi.Response(
                'Respuesta exitosa de todos los contactos.',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'estado': openapi.Schema(type=openapi.TYPE_STRING, example='ok'),
                        'mensaje': openapi.Schema(type=openapi.TYPE_STRING, example='listados con exito'),
                        'data': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT))
                    }
                )
            )
        }
    )
    def get(self, request, *args, **kwargs):
        #se sobreescribe el metodo 'list' para manetenr la estructura
        #de respuesta  personalizada
        data = Contacto.objects.order_by('-id').all()
        serializer = ContactoSerializer(data, many=True, context={'request': request})    
        return Response({
            'estado': 'ok',
            'mensaje': 'listados con exito',
            'data': serializer.data   
        }, status=status.HTTP_200_OK)

    
""" data = Contacto.objects.order_by('-id').all()
        serializer = ContactoSerializer(data, many=True, context={'request':request})    
        return Response({"estado": "ok", "mensaje": "listados con exito", "data": serializer.data}, status=status.HTTP_200_OK)
        """
        
        
        
        
        
        
            
            
            
