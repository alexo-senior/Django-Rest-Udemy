from django.urls import path
from .views import *

#se crea la ruta en la url de la app categoria
urlpatterns = [
    path('contacto',Clase1.as_view()),
    
    
]