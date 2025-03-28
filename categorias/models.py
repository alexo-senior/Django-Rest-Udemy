from django.db import models
from autoslug import AutoSlugField

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    #AutoSlugField genera automáticamente un slug basado en otro campo de tu modelo. Esto es muy útil porque te evita tener que crear y mantener slugs manualmente
    slug = AutoSlugField(populate_from='nombre')#el campo populate_from le dice al autslug que campo va a ser el que se va a tomar para generar el slug
    
    #esta es una funcion de ayuda para que nos muestre el nombre de la categoria por defecto
    def __str__(self):
        return self.nombre
    
    #generar una subclase para generar datos meta
    #una version en singular y otra en plural
    class Meta:
        db_table = 'categorias'#indica el nombre de la tabla en el admon de django
        verbose_name = 'categoria'#variable singular
        verbose_name_plural = 'categorias'#varible plural
        
        
        
        
        
        
    
        
        
        
        
    