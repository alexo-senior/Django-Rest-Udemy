from django.urls import path
from .views import *

#se crea la ruta en la url de la app categoria
urlpatterns = [
    path('recetas',Clase1.as_view()),
    #path('categorias/<int:id>',Clase2.as_view()),
]


