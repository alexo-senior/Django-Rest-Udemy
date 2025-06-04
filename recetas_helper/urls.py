from django.urls import path
from .views import *
from .views import Clase1

#se crea la ruta en la url de la app categoria
#laas validaciones aqui no son aconsejables, es mejor en la vista 
urlpatterns = [
    path('recetas_panel/<int:id>',Clase4.as_view()),#se le pasa el id del usuario  
        
]
