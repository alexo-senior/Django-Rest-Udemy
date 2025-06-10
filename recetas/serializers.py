from rest_framework import serializers
from . models import *
from dotenv import load_dotenv
import os #para cargar las variables de entorno

#crear los serializadores
#SERIALIZER ES EL INTERPRETE PARA DAR UNA SALIDA LEGIBLE EN FORMATO JSON
#se crea la clase RecetaSerializer que hereda de serializers.ModelSerializer
from django.conf import settings

class RecetaSerializer(serializers.ModelSerializer):
    categoria = serializers.ReadOnlyField(source='categoria.nombre')
    fecha = serializers.DateTimeField(format="%d/%m/%Y")
    imagen = serializers.SerializerMethodField()
    #para que se puedan visualizar los datos del usuario
    user = serializers.ReadOnlyField(source="user.first_name")
    #user = serializers.ReadOnlyField(source="first_name")

    class Meta:
        model = Receta
        fields = ["id", "nombre", "slug", "tiempo", 
                "descripcion", "fecha", "categoria", 
                "categoria_id", "imagen", "user_id", "user"]

    def get_imagen(self, obj):
        request = self.context.get('request')
        if obj.foto:
            """Construye la URL absoluta usando MEDIA_URL y el request
            para que la imagen se pueda acceder desde el navegador o el frontend"""
            url = f"{settings.MEDIA_URL}recetas/{obj.foto}"
            if request is not None:
                return request.build_absolute_uri(url)
            else:
                # Fallback si no hay request en el contexto
                return f"{os.getenv('BASE_URL')}{url}"
        return None
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        
        
        
        
    
    