from django.urls import path
from .views import *


urlpatterns = [
    path('', home_inicio, name='home' )#se puede colocar asi sin el name, el nombre debe ser igual al ded la vista
    
]


