from django.db import models
from django.contrib.auth.models import User
#este modelo user tiene todos los campos contenidos en la tabla de usuarios
#auth_user
class UsersMetadata(models.Model):
    #agregamos la llave foranea de la tabla de usuarios
    user = models.ForeignKey(User, models.DO_NOTHING)
    #es un token sencillo que permite la autenticacion de los usuarios
    #se recomienda que sea un token de 50 caracteres
    token = models.CharField(max_length=50, blank=True, null=True)  
    #se peuden agregar otros campos como el nombre, apellido, etc
    
    def __str__(self):
        return f"{self.first_user} {self.last_name}"
    
    class Meta:
        db_table = 'users_metadata'
        verbose_name = 'User_Metadata'
        verbose_name_plural = 'Users_Metadata'
        
        
        
        
        
    
    
