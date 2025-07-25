from django.db import models
from datetime import datetime
#from django.utils import timezone



class Contacto(models.Model):
    nombre = models.CharField(max_length=100, blank=True)
    correo = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=100, blank=True)
    mensaje = models.TextField()
    #el auto_now=True se usa para que se guarde la fecha y hora actual al crear el objeto
    #pero trabaja con la fecha de la base de de datos, no con la del servidor
    fecha = models.DateTimeField(auto_now=True)
    
    #fecha = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.nombre
    

    class Meta:
        db_table = 'contacto'
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        
        






