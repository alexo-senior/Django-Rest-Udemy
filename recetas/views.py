from django.shortcuts import render
from http import HTTPStatus 
from django.http import JsonResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response  # Importa Response
from .serializers import RecetaSerializer
from .models import *
from rest_framework import status #import status
from django.utils.dateformat import DateFormat
import os
from dotenv import load_dotenv
from datetime import datetime
#la importacion es para manejar los archivos multimedia
from django.core.files.storage import FileSystemStorage
from seguridad.decorators import logueado
from jose import jwt
from django.conf import settings 
from django.utils.text import slugify
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema









# Create your views here.
"""class Clase1(APIView):
    def get(self, request):
        #se obtiene el id de la receta desde el ultimo id de la base de datos
        #se ordena de forma descendente para obtener el ultimo id
        data = Receta.objects.order_by('-id').all()
        #se crea una variable que contiene el serializador de recetasserializer
        datos_json = RecetaSerializer(data, many=True)
        #se retorna un json con el contenido de la variable datos_json
        #el metodo data convierte el objeto en un diccionario de python
        return JsonResponse({"data": datos_json.data})"""
        
        
#LA CLASE1 SE TOMA PARA LOS GET Y POST YA QUE NO REQUIERE ID

    
            
            
            
class Clase1(APIView):
    @swagger_auto_schema(
        request_body=RecetaSerializer,
        operation_description="crear una nueva receta",
        responses={201:"receta ceada con exito",
                400:"errorr de validacion"}
    )
            
    #METODO POST PARA CREAR UNA NUEVA RECETA 
    #TENER EN CUENTA A MI PARECER QUE SOLO ACTUALIZA POR NOMBRE DE LA RECETA
    @logueado()
    #decorador para que solo se pueda acceder a esta vista si el usuario esta logueado
    
    def post(self, request):
        serializer = RecetaSerializer(data= request.data)
        if not serializer.is_valid():
            return Response({"estado": "error", "mensaje": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
            
        """validacion de los campos parra la receta, con un bucle for
        se hace mas sencillo y evita repetir codigo"""
        
        campos_obligatorios = ["nombre", "tiempo", "descripcion", "categoria_id", "foto"]
        for campo in campos_obligatorios:
            if not request.data.get(campo):
                return Response({"estado": "error", "mensaje": f"el campo {campo} es obligatorio"},
                                status=status.HTTP_400_BAD_REQUEST)
                
        """valida primero la existencia de la categoria"""
        
        if not Categoria.objects.filter(pk=request.data["categoria_id"]).exists():
            return Response({"estado":"error", "mensaje": "la categoria no existe"},
                    status=HTTPStatus.BAD_REQUEST)
            
        """valida el nombre de la receta, si ya existe no se puede crear con ese nombre""" 
        
        if Receta.objects.filter(nombre=request.data["nombre"]).exists():
                #hago un retorno con un format para que salga mas especifica la busqueda errada
                #el format en la respuesta de errores no es recomendable por la seguridad 
            return Response({"estado": "error", "mensaje": f"El nombre{request.data['nombre']} no está disponible"}, 
                            status=HTTPStatus.BAD_REQUEST)
            
        """validar y guardar la foto"""     
        try:
            fecha = datetime.now()  # Define 'fecha' with the current datetime
            foto = f"{datetime.timestamp(fecha)}{os.path.splitext(str(request.FILES['foto']))[1]}"
        except Exception as e:
            return Response({"estado":"error", "mensaje":f"debe adjuntar una foto {str(e)}"},
                                status=HTTPStatus.BAD_REQUEST)
            
        """mimetime"""
        if request.FILES["foto"].content_type not in ["image/jpeg", "image/png"]:
            return Response({"estado": "error", "mensaje": "Formato de imagen no valido"},
                            status=status.HTTP_400_BAD_REQUEST)
                            
        try:
            fs = FileSystemStorage()
                
            fs.save(f"recetas/{foto}",request.FILES['foto'])
                
            #retorna la url del archivo y hace el guardado de forma completa
            
            fs.url(request.FILES['foto'])
            
        except Exception as e:
            return Response({"estado":"error", "mensaje":f"se produjo un error al subir el archivo {str(e)}"},
                                    status=HTTPStatus.BAD_REQUEST)
        
        header = request.headers.get('Authorization', '').split(" ")    
        if len(header) != 2:
            return Response({"estado": "error", "mensaje": "Token de autorización inválido"},
                            status=status.HTTP_401_UNAUTHORIZED)
        try:
            resuelto = jwt.decode(header[1], settings.SECRET_KEY, algorithms=['HS512'])
        except Exception as e:
            return Response({"estado": "error", "mensaje": f"Token inválido: {str(e)}"},
                            status=status.HTTP_401_UNAUTHORIZED)
                                
        slug= slugify(request.data["nombre"])
        try:
            # luego si no existe se crea la receta con create
            Receta.objects.create(
                    nombre=request.data["nombre"],
                    tiempo=request.data["tiempo"],
                    descripcion=request.data["descripcion"],
                    categoria_id=request.data["categoria_id"],  # Corregido
                    foto= foto, 
                    user_id=resuelto["id"]  # Asignar el ID del usuario desde el token
                    # Asignar slug si se proporciona
                        )
            
            return Response({"estado":"ok",
                    "mensaje": "Receta creada exitosamente"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
                # Captura errores durante la creación de la receta
                # y devuelve un error 500 Internal Server Error
                return Response(
                    {"error": f"Error al crear la receta: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    """obtener las recetas de forma general"""        
    
    def get(self, request):
        try:
            """consulta los objetos receta ordenados de forma descendente por id"""
            data = Receta.objects.order_by('-id').all()

            if not data:
                return Response(status=status.HTTP_204_NO_CONTENT)  # Devuelve 204 si no hay datos

            datos_json = RecetaSerializer(data, many=True)
            return Response({"data": datos_json.data}, status=status.HTTP_200_OK)  # Devuelve 200 OK
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        
                    
        
        
        
                
    
            
        
        
            


            
#CONSULTAR RECETA POR ID            
#LA CLASE2 SE TOMA PARA LOS GET, PUT  Y DELETE YA QUE REQUIERE ID   
class Clase2(APIView):
    def get(self, request, id):
        try:
            # Consulta los objetos receta por id
            data = Receta.objects.filter(id=id).get()
            
            if not data:
                # Si no hay datos, devuelve un 204 no content
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            # Formateo de todos los datos de la receta
            return Response({
                "data": {
                    "id": data.id,
                    "nombre": data.nombre,
                    "slug": data.slug,
                    "tiempo": data.tiempo,
                    "descripcion": data.descripcion,
                    "fecha": DateFormat(data.fecha).format("d/m/Y"),
                    "categoria_id": data.categoria_id,
                    "imagen": f"{os.getenv('BASE_URL')}uploads/recetas/{data.foto}",
                    "user_id": data.user_id, "user":data.user.first_name 
                }#lista ademas de los datos de la receta el nombre del usuario y el id del usuario 
            }, status=status.HTTP_200_OK)
        except Receta.DoesNotExist:
            return Response({"estado": "error", "mensaje": "la receta no existe"},
                    status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Maneja cualquier error de servidor
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                                    
            
            
            
    #METODO PUT PARA ACTUALIZAR UNA RECETA POR ID    
    def put(self, request, id):
        # Validaciones antes de buscar la receta
        if request.data.get("nombre") is None or not request.data["nombre"]:
            return Response({"estado": "error", "mensaje": "el campo nombre es obligatorio"}, 
                            status=HTTPStatus.BAD_REQUEST)

        if request.data.get("tiempo") is None or not request.data["tiempo"]:
            return Response({"estado": "error", "mensaje": "el campo tiempo es obligatorio"}, 
                            status=HTTPStatus.BAD_REQUEST)

        if request.data.get("descripcion") is None or not request.data["descripcion"]:
            return Response({"estado": "error", "mensaje": "el campo descripcion es obligatorio"}, 
                            status=HTTPStatus.BAD_REQUEST)

        if request.data.get("categoria_id") is None or not request.data["categoria_id"]:
            return Response({"estado": "error", "mensaje": "el campo categoria_id es obligatorio"}, 
                            status=HTTPStatus.BAD_REQUEST)

        # Validar que la categoría exista antes de actualizar
        # Se usa filter() y get() para obtener el objeto de la categoría
        try:
            categoria = Categoria.objects.get(pk=request.data["categoria_id"])
        except Categoria.DoesNotExist:
            return Response({"estado": "error", "mensaje": "la categoria no existe"},
                            status=HTTPStatus.BAD_REQUEST)

        # Buscar la receta
        try:
            receta = Receta.objects.get(id=id)
        except Receta.DoesNotExist:
            return Response({"mensaje": "receta no existe"}, status=status.HTTP_404_NOT_FOUND)

        # Actualizar los campos de la receta
        receta.nombre = request.data.get("nombre", receta.nombre)
        receta.tiempo = request.data.get("tiempo", receta.tiempo)
        receta.descripcion = request.data.get("descripcion", receta.descripcion)
        receta.categoria = categoria  # Asigna el objeto de la categoría

        # Guardar los cambios
        try:
            receta.save()
            return Response({"mensaje": "receta actualizada correctamente"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            
            
    #METODO PARA ELIMINAR REGISTROS POR ID
    #ESTE METODO ES PARA BORRAR SOLO LAS RECETAS NO DED LA BASE DE DATOS
    #NI BORRAR LA FOTO
    
    """def delete(self, request, id):
        try:
            #primero verrifica si la receta existe
            receta = Receta.objects.get(id=id)
            #elimina la receta
            receta.delete()
            return Response({"estado": "ok", "mensaje":"receta eliminada corrrectamente"},
                            status=status.HTTP_200_OK)
            
        except Receta.DoesNotExist:
            return Response({"estado": "error", "mensaje": "la receta no existe"},
                            status=status.HTTPSTTP_404_NOT_FOUND)
        #maneja cualquier error    
        except Exception as e:
            return Response ({"error": str(e)}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            """
            
            
    def delete(self, request, id):
        try:
            data = Receta.objects.get(id=id)
        except Receta.DoesNotExist:
            return Response({"estado": "error", "mensaje": "la receta no existe"}, 
                        status=status.HTTP_404_NOT_FOUND)
        #borrar la foto
        #al dar el punto se le indica que la foto esta en el directrio uploads/recetas
        # (raiz del proyecto)
        os.remove(f"./uploads/recetas/{data.foto}")
        #borrar la receta de la base de datos aunque no se debe hacer
        #se usa el metodo filter() para filtrar los objetos de la receta por id 
        # y luego se usa el metodo delete() para eliminar el objeto
        Receta.objects.filter(id=id).delete()
        return Response({"estado": "ok", "mensaje":"receta eliminada correctamente"}, 
                    status=status.HTTP_200_OK)
    
    





            
        
            
            
            
            
            
            
        
            
            
                
        
        
            
        
        
        
            
        
            
            
            
            
    
    
    
    
    