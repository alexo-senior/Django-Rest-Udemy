from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, Http404, HttpResponseRedirect
from seguridad.decorators import logueado
from django.contrib.auth.models import User

#las recetas deben ir asociadas a un usuario, por lo que se debe crear un modelo de usuario
#es aconsejable reservar el usuario numero 1 para el administrador 
#como nota se debe crear un metodo para proteger las vistas de recetas 
class Clase1(APIView):
    def get(self, request):
        pass
    
    
class Clase4(APIView):
    
    @logueado() 
    def get(self, request, id):
        #lo primero es validar que el id del usuario existe
        try:
            usuario_existe = User.objects.filter(pk=id).get()
        except User.DoesNotExist:
            return Response({"estado": "error", "mensaje": "ocurrio un error en la consulta"},
                    status=status.HTTP_404_NOT_FOUND) 
                    
            
            
            
    
    