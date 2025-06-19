from http import HTTPStatus
from rest_framework.response import Response
from django.utils.text import slugify
from rest_framework.views import APIView
from rest_framework import status
from .models import Categoria
from .serializers import CategoriaSerializer
from django.http import Http404
from recetas.models import Receta
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema

"""para que swagger sepa que campos esperar """
class CategoriaInputSerializer(serializers.Serializer):
    nombre = serializers.CharField()



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
        return Response({"data": data_json.data}, status=HTTPStatus.OK)
        #se puede hacer una respuesta tipo response para probar que los datos se estan mostrando correctamente
        #return Response(data)
        """configuracion para el swagger informacion del endpoint"""
    @swagger_auto_schema(
        request_body=CategoriaInputSerializer,
        operation_description="Endpoint para crear una nueva categoria de recetas",
        responses={
            201:"creada con exito",
            400: "Bad Request",
            404: "Not Found"
        }
        )    

        
        #SE CREA LA FUNCION PARA EL METODO POST
        
    def post(self, request):
        """Deserializador que recibe los datos del contacto de parte del cliente"""
        serializer = CategoriaInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"estado": "error", "mensaje":"serializer no valido"},status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
            nombre = serializer.validated_data['nombre']
            """para crear el slug de forma automatica """
            slug = slugify(nombre)
            Categoria.objects.create(nombre=nombre, slug=slug)
            return Response({"estado": "ok", "mensaje": "se crea el registro exitosamente"}, 
                            status=status.HTTP_201_CREATED)
        except Exception:
            return Response({"estado": "error", "mensaje": "ocurrió un error al guardar"}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
            
    """validaciones de datos de entrada"""
    """
    if request.data.get("nombre")==None or not request.data['nombre']:
        return Response({"estado":"error", "mensaje":"el campo nombre no puesde estar vacio"},
                            status= HTTPStatus.BAD_REQUEST)"""
        
                
            
                
        

#LISTAR UN REGISTRO POR SU ID
class Clase2(APIView):
    def get(self, request, id):
        try:
        #se puede usar tambien pk al consultar id o llave primaria
        #se usa get en vez de all() para que solo traiga los registros pedidos sin corchetes
            data = Categoria.objects.filter(id=id).get()
            return Response({'data':{'id':data.id,'nombre':data.nombre, 'slug':data.slug}}, status=HTTPStatus.OK)
        #se le agrega el manejo de errores try except, el DoesnotExist es el 
        #error que parece cuando no se encuentra el registro, por lo tanto lo puedes copiar
        except Categoria.DoesNotExist:  # Correcto
            raise Http404

        
    #MODIFICAR O EDITAR UN REGISTRO POR SU ID FUNCION PUT   
    @swagger_auto_schema(
        request_body=CategoriaInputSerializer,
        operation_description="Endpoint para crear una nueva categoria de recetas",
        responses={
            201:"creada con exito",
            400: "Bad Request",
            404: "Not Found"
        }
    )
    
    def put(self, request, id):
        serializer = CategoriaInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"estado": "error", "mensaje": serializer.errors}, status=400)
        nombre = request.data.get("nombre")
        #vallidar que el campo nombre no este vacio
        if not nombre:
            return Response({"estado":"error", "mensaje": "el campo nombre no puede estar vacio"}, 
            status= HTTPStatus.BAD_REQUEST)
        try:
            #analizar directamente el registro si existe
            data = Categoria.objects.get(id=id)
            data.nombre = nombre
            data.slug = slugify(nombre)
            data.save()
            
            #validacion para que el caso de exito al modificar el registro
            return Response({"estado": "ok", "mensaje": "se modifica el registro con exito"}, 
            status=HTTPStatus.OK)
            #validacion en caso de que no exista el registro
        except Categoria.DoesNotExist:
            return Response({"estado": "error" , "mensaje": "el registro no existe"}, 
            status=status.HTTP_404_NOT_FOUND)
            #validacion en caso que haya algun error
        except Exception as e:
            return Response({"estado": "error", "mensaje": "ocurrio un error"}, 
            status=HTTPStatus.INTERNAL_SERVER_ERROR) 
                                
                                
        
        
        #METODO DELETE FUNCION PARA ELIMINAR
        
    def delete(self, requesT, id):
        try:
        # Verificar si el registro existe antes de eliminarlo
            categoria = Categoria.objects.filter(id=id)
            if not categoria.exists():
                return Response(
                    {"estado": "error", "mensaje": "El registro no existe"},
                    status=status.HTTP_404_NOT_FOUND
            )
            if Receta.objects.filter(categoria_id=id).exists():
                return Response(
                    {"estado": "error", "mensaje": "No se puede eliminar la categoria porque tiene recetas asociadas"},
                    status=HTTPStatus.BAD_REQUEST
            )
        
        # Eliminar el registro
            categoria.delete()
            return Response(
                {"estado": "ok", "mensaje": "Se elimina el registro exitosamente"},
                status=HTTPStatus.OK
        )
        except Exception as e:
        # Manejo genérico de errores
            return Response(
                {"estado": "error", "mensaje": "Ocurrió un error inesperado"},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
            
            
            
            
            
        
        
        
        
        
    
        
        
        
        
                
            
                
        
        
        
        
        
        
        
    
    
        
    
    
    
    
        
        
        
    
    
    
