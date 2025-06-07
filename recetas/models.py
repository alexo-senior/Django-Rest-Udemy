from django.db import models
from autoslug import AutoSlugField
#no sirve usar .models ya que tomaria el modelo de la app recetas
#por eso se importa el modelo de categorias directamente
from categorias.models import Categoria
from django.contrib.auth.models import User


# Create your models here.
#LOS MODELOS SON LAS TABLAS DE MI BASE DE DATOS
class Receta(models.Model):
    #se crea una llave foranea para el usuario que creo la receta
    #se le coloca en default 1 para que no este vacia la relacion
    #la llave se cra para la relacion con la app de recetas_helper 
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    #se crea ademas llave foranea para relacionar las recetas a las categorias enteriores
    
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='recetas')
    
    nombre = models.CharField(max_length=100, null=False)
    
    #AutoSlugField genera automáticamente un slug basado en otro campo de tu modelo. Esto es muy útil porque te evita tener que crear y mantener slugs manualmente
    #el campo populate_from le dice al autslug que campo va a ser el que se va a tomar para generar el slug
    
    slug = AutoSlugField(populate_from='nombre', max_length=50 )
    tiempo = models.CharField(max_length=100, null=True)
    #solo para guardar el nombre no la foto como tal no el archivo en si
    foto = models.CharField(max_length=100, null=True)
    #sin tildes ni caracteres especiales, texfield para mucho texto
    descripcion = models.TextField()
    #para configurar la fecha ded forma automatica
    fecha = models.DateTimeField(auto_now_add=True, null=True)
    
    
    
    
    
    
    #esta es una funcion de ayuda para que nos muestre el nombre de la categoria por defecto
    def __str__(self):
        return self.nombre
    
    #generar una subclase para generar datos meta
    #una version en singular y otra en plural
    class Meta:
        db_table = 'recetas'#indica el nombre de la tabla en el admon de django
        verbose_name = 'Receta'#variable singular
        verbose_name_plural = 'Recetas'#varible plural
        
        
        
        
        
        
    
        
        
        

# Create your models here.
