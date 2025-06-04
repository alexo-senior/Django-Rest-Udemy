from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, Http404, HttpResponseRedirect
from seguridad.decorators import logueado
from django.contrib.auth.models import User
from recetas.models import * 
from recetas.serializers import RecetaSerializer
#Este metodo es solo para usuarios logeados  
#las recetas deben ir asociadas a un usuario, por lo que se debe crear un modelo de usuario
#es aconsejable reservar el usuario numero 1 para el administrador 
#como nota se debe crear un metodo para proteger las vistas de recetas 
class Clase1(APIView):
    def get(self, request):
        pass
    
    
class Clase4(APIView):
    
    @logueado() 
    def get(self, request, id):
        #validar que el id del usuario existe
        try:
            usuario_existe = User.objects.filter(pk=id).get()
        except User.DoesNotExist:
            return Response({"estado": "error", "mensaje": "ocurrio un error en la consulta"},
                    status=status.HTTP_404_NOT_FOUND) 
            ##se obtiene el id del usuario logueado validando que exista
        data = Receta.objects.filter(user_id=id).order_by('-id').all()
        #se crea una variable serializer para los datos de la receta      
        datos_json = RecetaSerializer(data, many=True)
        return Response({"data":datos_json.data },status=status.HTTP_200_OK)
                        
        
        
        
                    
            
            
            
    
    