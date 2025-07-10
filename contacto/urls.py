from django.urls import path
from .views import *
from .views import ContactoListView

#se crea la ruta en la url de la app categoria
urlpatterns = [
    path('contacto',Clase1.as_view()),
    path('contactos/', ContactoListView.as_view(), name='contacto-list'),
    
    
]