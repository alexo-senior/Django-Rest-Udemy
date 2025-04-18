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
            
            
            
            
    #METODO POST PARA CREAR UNA NUEVA RECETA 
    #TENER EN CUENTA A MI PARECER QUE SOLO ACTUALIZA POR NOMBRE DE LA RECETA       
    def post(self, request):
        #validacion de cada campo esta vez el campo nombre
        if request.data.get("nombre") == None or not request.data["nombre"]:
            
            return Response({"estado":"error", "mensaje": "el campo nombre es obligatorio"}, 
                        status=HTTPStatus.BAD_REQUEST)
        
        if request.data.get("tiempo") == None or not request.data["tiempo"]:
            return Response({"estado":"error", "mensaje": "el campo tiempo es obligatorio"}, 
                        status=HTTPStatus.BAD_REQUEST)
        
        if request.data.get("descripcion") == None or not request.data["descripcion"]:
            return Response({"estado":"error", "mensaje": "el campo descripcion es obligatorio"}, 
                        status=HTTPStatus.BAD_REQUEST)
            
        if request.data.get("categoria_id") == None or not request.data["categoria_id"]:
            return Response({"estado":"error", "mensaje": "el campo categoria_id es obligatorio"}, 
                            
                        status=HTTPStatus.BAD_REQUEST)
        #validar que la categoria exista, no se usa ids porque no es el nombre de la categoria
        #se usa el metodo filter() para filtrar los objetos de la categoria por id y luego se usa el metodo get() para obtener el objeto
        try:
            categoria = Categoria.objects.filter(pk=request.data["categoria_id"]).get()
        except Categoria.DoesNotExist:
            return Response({"estado":"error", "mensaje": "la categoria no existe"},
                            status=HTTPStatus.BAD_REQUEST)
            
            
        
        try:
            #primero se valida si la receta ya existe por el nombre con filter() y exist()
            if Receta.objects.filter(nombre=request.data["nombre"]).exists():
                #hago un retorno con un format para que salga mas especifica la busqueda errada
                #el format en la respuesta de errores no es recomendable por la seguridad 
                return Response(
                    {"estado": "error", "mensaje": f"El nombre{request.data["nombre"]} no esta disponible"},
                    status=HTTPStatus.BAD_REQUEST)
            #modulo para manejar las imagenes    
            fs = FileSystemStorage()
            
            try:
                fecha = datetime.now()  # Define 'fecha' with the current datetime
                foto = f"{datetime.timestamp(fecha)}{os.path.splitext(str(request.FILES['foto']))[1]}"
            except Exception as e:
                return Response({"estado":"error", "mensaje":f"debe adjuntar una foto {str(e)}"},
                                status=HTTPStatus.BAD_REQUEST)
            try:
                fs.save(f"ejemplo/{foto}",request.FILES['foto'])
        #retorna la url del archivo y hace el guardado de forma completa
                fs.url(request.FILES['foto'])
            except Exception as e:
                return Response({"estado":"error", "mensaje":f"se produjo un error al subir el archivo {str(e)}"},
                                status=HTTPStatus.BAD_REQUEST)
            
                
            #luego si no existe se crea la receta con create
            Receta.objects.create(
                    nombre=request.data["nombre"],
                    tiempo=request.data["tiempo"],
                    descripcion=request.data["descripcion"],
                    categoria_id=request.data["categoria_id"],  # Corregido
                    foto= foto 
                )

            return Response(
                {"message": "Receta creada exitosamente"},
                        status=status.HTTP_201_CREATED
            )

        except Categoria.DoesNotExist:
            return Response(
                {"error": "La categoría especificada no existe."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": f"Error al crear la receta: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
            
            
#CONSULTAR RECETA POR ID            
#LA CLASE2 SE TOMA PARA LOS GET, PUT  Y DELETE YA QUE REQUIERE ID   
class Clase2(APIView):
    def get(self, request, id):
        try:
            #consulta los objetos receta por id
            data = Receta.objects.filter(id=id).get()
            
            if not data:
            #si no hay datos devuelve un 204 no content
                return Response(status=status.HTTP_204_NO_CONTENT)
            #formateo de todos los datos de la receta, entonces por medio del id se obtiene la receta 
            return Response({"data":{"id":data.id, "nombre":data.nombre, "slug":data.slug, "tiempo":data.tiempo,
                                    "descripcion":data.descripcion, "fecha":DateFormat(data.fecha).format("d/m/Y"),
                                    "categoria_id":data.categoria_id, "imagen":f"{os.getenv('BASE_URL')}uploads/recetas/{data.foto}"}}, 
                            status=status.HTTP_200_OK)
                                    
                                    
            #return Response({"data": datos_json.data}, status=status.HTTP_200_OK)
        except Receta.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #maneja la excepcion en caso de error de servidor
        except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    #METODO PUT PARA ACTUALIZAR UNA RECETA POR ID    
    def put(self, request, id):
        try:
            receta = Receta.objects.get(id=id)
            
            # Actualiza los campos de la receta con los datos proporcionados
            receta.nombre = request.data.get("nombre", receta.nombre)
            receta.tiempo = request.data.get("tiempo", receta.tiempo)
            receta.descripcion = request.data.get("descripcion", receta.descripcion)
            receta.categoria_id = request.data.get("categoria_id", receta.categoria_id)
            
            # Guarda los cambios
            receta.save()
            return Response({
                    "mensaje":"rececta actualizada correctament"
                }, status=status.HTTP_200_OK)
        except Receta.DoesNotExist:
                return Response({
                    "mensaje": "receta no existe"
                })
                
        except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
    #METODO PARA ELIMINAR REGISTROS POR ID
    
    def delete(self, request, id):
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
            
            
            
            
        
            
            
                
        
        
            
        
        
        
            
        
            
            
            
            
    
    
    
    
    