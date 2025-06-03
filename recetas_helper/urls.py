from django.urls import path
from .views import *
from .views import Clase1

#se crea la ruta en la url de la app categoria
urlpatterns = [
    path('recetas-panel/<int:id>',Clase4.as_view()),#se le pasa el id del usuario  
        
]
