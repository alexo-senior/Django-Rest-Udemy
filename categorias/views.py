from django.shortcuts import render
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.response import Response
from . models import Categoria
from . serializers import CategoriaSerializer
from http import HTTPStatus
from django.http import Http404



#se crea la clase Clase1 que hereda de APIView. 
class Clase1(APIView):
    def get(self, request):
        #se crea la variable data que contiene todos los datos de la tabla Categoria
        #para eso se debe importar primero la tabla Categoria
        #luego se usa el metodo objects.order_by('-id').all() para que los datos se ordenen por id de forma descendente
        data = Categoria.objects.order_by('-id').all()
        data_json = CategoriaSerializer(data, many=True)
        #return Response(data_json.data)
        #la forma correcta es usa json_Response por seguridad de los datos
        #return JsonResponse(data_json.data)
        #se puede envolver en un objeto llamado data para que se vea mas ordenado
        #y de esa forma se visualiza en la web para probar que los datos se estan mostrando correctamente
        return JsonResponse({"data": data_json.data}, status=HTTPStatus.OK)
        #se puede hacer una respuesta tipo response para probar que los datos se estan mostrando correctamente
        #return Response(data)

#listar un registro por su id
class Clase2(APIView):
    def get(self, request, id):
        try:
        #se puede usar tambien pk al consultar id o llave primaria
        #se usa get en vez de all() para que solo traiga los registros pedidos
            data = Categoria.objects.filter(id=id).get()
            return JsonResponse({'data':{'id':data.id,'nombre':data.nombre, 'slug':data.slug}}, status=HTTPStatus.OK)
        #se le agrega el manejo de errores try except, el DoesnotExist es el 
        #error que parece cuando no se encuentra el registro, por lo tanto lo puedes copiar
        except Categoria.DoesnotExist:
            raise Http404
        
    
    
        
    
    
    
    
        
        
        
    
    
    
