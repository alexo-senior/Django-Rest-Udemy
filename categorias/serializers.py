from rest_framework import serializers
from . models import *

#crear los serializadores
#se crea la clase CategoriaSerializer que hereda de serializers.ModelSerializer
class CategoriaSerializer(serializers.ModelSerializer):
    #se crea una clase meta que hereda de la clase Categoria
    #el modelo es la categoria a la que queremos conectarnos
    class Meta:
        model = Categoria
        fields = '__all__'
    #se puede hacer de esta otra forma tambien
    #fields = ['id', 'nombre', 'slug']
    
    
    
    
    
    
    
    