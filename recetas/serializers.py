from rest_framework import serializers
from . models import *

#crear los serializadores
#se crea la clase RecetaSerializer que hereda de serializers.ModelSerializer
class RecetaSerializer(serializers.ModelSerializer):
    #se crea una variable categoria que sera de lectura de solo el campo nombre de la categoria
    #el source indica que el campo categoria se va a tomar del modelo Receta y de la propiedad nombre de la categoria
    categoria = serializers.ReadOnlyField(source='categoria.nombre')
    fecha = serializers.DateTimeField(format="%d/%m/%Y")
    #Meta es una clase interna que se utiliza para definir metadatos para el serializador
    
    
    class Meta:
        #indica el modelo que se va a utilizar
        model = Receta
        #fields = '__all__'
    #se puede hacer de esta otra forma tambien
        fields = ["id", "nombre", "slug", "tiempo",  "descripcion", "fecha", "categoria", "categoria_id"]
        
    
    