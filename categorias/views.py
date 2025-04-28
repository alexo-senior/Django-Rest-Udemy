from http import HTTPStatus
from django.http.response import JsonResponse
from django.utils.text import slugify
from rest_framework.views import APIView
from .models import Categoria
from .serializers import CategoriaSerializer
from django.http import Http404
from recetas.models import Receta





#se crea la clase Clase1 que hereda de APIView. 
class Clase1(APIView):
    def get(self, request):
        #se crea la variable data que contiene todos los datos de la tabla Categoria
        #para eso se debe importar primero la tabla Categoria
        #luego se usa el metodo objects.order_by('-id').all() para que los datos se ordenen por id de forma descendente
        data = Categoria.objects.order_by('-id').all()
        data_json = CategoriaSerializer(data, many=True)
        #return Response(data_json.data)
        #return JsonResponse(data_json.data)
        #se puede envolver en un objeto llamado data para que se vea mas ordenado
        #y de esa forma se visualiza en la web para probar que los datos se estan mostrando correctamente
        return JsonResponse({"data": data_json.data}, status=HTTPStatus.OK)
        #se puede hacer una respuesta tipo response para probar que los datos se estan mostrando correctamente
        #return Response(data)


        
        #SE CREA LA FUNCION PARA EL METODO POST
    def post(self, request):
        #validacion para que el campo nombre no este vacio
        if request.data.get("nombre")==None or not request.data['nombre']:
            return JsonResponse({"estado":"error", "mensaje":"el campo nombre no puesde estar vacio"},
                                status= HTTPStatus.BAD_REQUEST)
        try:
        # Se crea un nuevo registro en la tabla Categoria solo enviando el nombre
            Categoria.objects.create(nombre=request.data['nombre'])
            # Se retorna una respuesta JsonResponse con un mensaje de éxito y un estado 201
            return JsonResponse({"estado": "ok", "mensaje": "se crea el registro exitosamente"}, 
                            status=HTTPStatus.CREATED)
        except Exception as e:
            raise Http404
        
                
            
                
        

#LISTAR UN REGISTRO POR SU ID
class Clase2(APIView):
    def get(self, request, id):
        try:
        #se puede usar tambien pk al consultar id o llave primaria
        #se usa get en vez de all() para que solo traiga los registros pedidos sin corchetes
            data = Categoria.objects.filter(id=id).get()
            return JsonResponse({'data':{'id':data.id,'nombre':data.nombre, 'slug':data.slug}}, status=HTTPStatus.OK)
        #se le agrega el manejo de errores try except, el DoesnotExist es el 
        #error que parece cuando no se encuentra el registro, por lo tanto lo puedes copiar
        except Categoria.DoesNotExist:  # Correcto
            raise Http404

        
    #MODIFICAR O EDITAR UN REGISTRO POR SU ID FUNCION PUT   
    def put(self, request, id):
        nombre = request.data.get("nombre")
        #vallidar que el campo nombre no este vacio
        if not nombre:
            return JsonResponse({"estado":"error", "mensaje": "el campo nombre no puede estar vacio"}, 
            status= HTTPStatus.BAD_REQUEST)
        try:
            #analizar directamente el registro si existe
            data = Categoria.objects.get(id=id)
            data.nombre = nombre
            data.slug = slugify(nombre)
            data.save()
            #validacion para que el caso de exito al modificar el registro
            return JsonResponse({"estado": "ok", "mensaje": "se modifica el registro con exito"}, 
            status=HTTPStatus.OK)
            #validacion en caso de que no exista el registro
        except Categoria.DoesNotExist:
            return JsonResponse({"estado": "error" , "mensaje": "el registro no existe"}, 
            status=HTTPStatus.NOT_FOUND)
            #validacion en caso que haya algun error
        except Exception as e:
            return JsonResponse({"estado": "error", "mensaje": "ocurrio un error"}, 
            status=HTTPStatus.INTERNAL_SERVER_ERROR) 
                                
                                
        
        
        #METODO DELETE FUNCION PARA ELIMINAR
        
    def delete(self, requesT, id):
        try:
        # Verificar si el registro existe antes de eliminarlo
            categoria = Categoria.objects.filter(id=id)
            if not categoria.exists():
                return JsonResponse(
                    {"estado": "error", "mensaje": "El registro no existe"},
                    status=HTTPStatus.NOT_FOUND
            )
            if Receta.objects.filter(categoria_id=id).exists():
                return JsonResponse(
                    {"estado": "error", "mensaje": "No se puede eliminar la categoria porque tiene recetas asociadas"},
                    status=HTTPStatus.BAD_REQUEST
            )
        
        # Eliminar el registro
            categoria.delete()
            return JsonResponse(
                {"estado": "ok", "mensaje": "Se elimina el registro exitosamente"},
                status=HTTPStatus.OK
        )
        except Exception as e:
        # Manejo genérico de errores
            return JsonResponse(
                {"estado": "error", "mensaje": "Ocurrió un error inesperado"},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
            
            
            
            
            
        
        
        
        
        
    
        
        
        
        
                
            
                
        
        
        
        
        
        
        
    
    
        
    
    
    
    
        
        
        
    
    
    
