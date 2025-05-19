from django.urls import path
from .views import  *




#from .views import *



urlpatterns = [
    path('seguridad/registro',Clase1.as_view()),
    #verificacion recibe un argumebto de tipo string
    path('seguridad/verificacion/<str:token>',Clase2.as_view()),
    
    
]



