from django.urls import path
from .views import Clase1



#from .views import *


#se crea la ruta en la url de la app categoria
urlpatterns = [
    path('seguridad/registro',Clase1.as_view()),
    
    
]
