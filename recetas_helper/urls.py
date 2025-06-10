from django.urls import path
from .views import *


#se crea la ruta en la url de la app categoria
#laas validaciones aqui no son aconsejables, es mejor en la vista 
urlpatterns = [
    path('recetas/editar/foto', Clase1.as_view()),
    path('recetas/slug/<str:slug>', Clase2.as_view()),
     path('recetas-home', Clase3.as_view()),
    path('recetas_panel/<int:id>', Clase4.as_view()),
    
]





