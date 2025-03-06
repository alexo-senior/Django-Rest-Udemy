from django.urls import path
from .views import Class_Ejemplo, Class_Ejemplo_Parametros, Class_EjemploUpload
#tambien se puedee colocar un asterisco en la importacion de las clases para que se importen todas las clases
#from .views import *




urlpatterns = [
    path('ejemplo', Class_Ejemplo.as_view()),
    path('ejemplo/<int:id>',Class_Ejemplo_Parametros.as_view()),
    #ruta para id como string
    path('ejemplo/<str:id>',Class_Ejemplo_Parametros.as_view()),
    path('ejemplo-upload', Class_EjemploUpload.as_view()),
]
