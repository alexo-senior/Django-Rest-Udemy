from django.shortcuts import render
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.response import Response
from . models import Categoria
from . serializers import CategoriaSerializer
from http import HTTPStatus
from django.http import Http404
from django.utils.text import slugify





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
            return JsonResponse({"estado": "ok", "mensaje": "se crea el registro exitosamente"}, status=HTTPStatus.CREATED)
        except Exception as e:
            raise Http404
        
                
            
                
        

#listar un registro por su id
class Clase2(APIView):
    def get(self, request, id):
        try:
        #se puede usar tambien pk al consultar id o llave primaria
        #se usa get en vez de all() para que solo traiga los registros pedidos sin corchetes
            data = Categoria.objects.filter(id=id).get()
            return JsonResponse({'data':{'id':data.id,'nombre':data.nombre, 'slug':data.slug}}, status=HTTPStatus.OK)
        #se le agrega el manejo de errores try except, el DoesnotExist es el 
        #error que parece cuando no se encuentra el registro, por lo tanto lo puedes copiar
        except Categoria.DoesnotExist:
            raise Http404
        
        
    def put(self, request, id):
        if request.data.get("nombre")==None:
            return JsonResponse({"estado":"error", "mensaje":"el campo nombre no puesde estar vacio"},
            status= HTTPStatus.BAD_REQUEST)
            
        if not request.data.get("nombre"):
            return JsonResponse({"estado":"error", "mensaje":"el campo nombre no puesde estar vacio"},
            status= HTTPStatus.BAD_REQUEST)
            #se recomienda colocar una excepcion
        try:
            data = Categoria.objects.filter(id=id).get()#pk es lo mismo que id
            #se obtiene por filter de la categoria el id y por medio de update 
            #se actualiza el nombre solamente al que pertenece el id
            Categoria.objects.filter(id=id).update(nombre=request.data.get('nombre'), 
            slug=slugify(request.data.get('nombre')))
            return JsonResponse({"estado": "ok", "mensaje": "se modifica el registro exitosamente"}, 
            status=HTTPStatus.OK)
        except Categoria.DoesNotExist:
            raise Http404
                
            
                
        
        
        
        
        
        
        
    
    
        
    
    
    
    
        
        
        
    
    
    
