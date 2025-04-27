from rest_framework import serializers
from . models import *
from dotenv import load_dotenv
import os #para cargar las variables de entorno

#crear los serializadores
#SERIALIZER ES EL INTERPRETE PARA DAR UNA SALIDA LEGIBLE EN FORMATO JSON
#se crea la clase RecetaSerializer que hereda de serializers.ModelSerializer
class RecetaSerializer(serializers.ModelSerializer):
    #ESTO ES FORMATEAR INFORMACION 
    #se crea una variable categoria que sera de lectura de solo el campo nombre de la categoria
    #el source indica que el campo categoria se va a tomar del modelo Receta y de la propiedad nombre de la categoria
    categoria = serializers.ReadOnlyField(source='categoria.nombre')
    fecha = serializers.DateTimeField(format="%d/%m/%Y")
    imagen = serializers.SerializerMethodField()
    
    
    class Meta:
        #indica el modelo que se va a utilizar
        model = Receta
        #fields = '__all__'
    #se puede hacer de esta otra forma tambien
        fields = ["id", "nombre", "slug", "tiempo",  "descripcion", "fecha", "categoria", "categoria_id",
                "imagen"]
        
    def get_imagen(self, obj):
        #prueba para ver ejemplos en el insomnia
        #return f"hola mundo{obj. id}"
        #cargar las variables de entorno como BASE_URL, uploads que contiene la foto de la receta
        #es decir cargar uploads de receetas y obj.foto
        load_dotenv()#para cargar las variables de entorno, esta vez BASE_URL
        #se carga la variable de entorno BASE_URL que contiene la url base de la api
        #y se retorna la url completa de la imagen de la receta
        return f"{os.getenv('BASE_URL')}uploads/recetas/{obj.foto}"
    
    
    
    
    
    
    
    
    
    
    
    

        
        
        
        
    
    