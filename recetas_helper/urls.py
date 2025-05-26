from django.urls import path
from .views import *
from .views import Clase1

#se crea la ruta en la url de la app categoria
urlpatterns = [
    path('recetas_h',Clase1.as_view()),
        
]
