from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, Http404, HttpResponseRedirect
from seguridad.decorators import logueado
from django.contrib.auth.models import User
from recetas.models import * 
from recetas.serializers import * 
from http import HTTPStatus
"""para subir los archivos al servidor"""
import os
from datetime import datetime 
from django.core.files.storage import FileSystemStorage
from dotenv import load_dotenv
from django.utils.dateformat import DateFormat


"""Este metodo es solo para usuarios logeados  
las recetas deben ir asociadas a un usuario, por lo que se debe crear un modelo de usuario
es aconsejable reservar el usuario numero 1 para el administrador 
como nota se debe crear un metodo para proteger las vistas de recetas """

"""Este metodo es para editar la foto de una receta
se debe validar que el usuario este logueado y que la receta exista"""

class Clase1(APIView):
    #el decorador se usa aqui para evitar que el metodo sea publico
    #y que sea solo para usuarios logueados 
    @logueado()
    def post(self, request):
        # Validar que el id existe
        if request.data.get("id") is None or not request.data.get("id"):
            return Response({"estado": "error", "mensaje": "el campo del id es obligatorio"},
                            status=status.HTTP_400_BAD_REQUEST)
        # Validar que la receta existe
        try:
            existe = Receta.objects.get(pk=request.data["id"])
            #me guardo la variable anterior para comparar 
            anterior = existe.foto
        except Receta.DoesNotExist:
            return Response({"estado": "error", "mensaje": "la receta no existe en la bd"},
                            status=status.HTTP_404_NOT_FOUND)

        # Creación y validación de la foto
        fs = FileSystemStorage()
        try:
            fecha = datetime.now()
            foto = f"{datetime.timestamp(fecha)}{os.path.splitext(str(request.FILES['foto']))[1]}"
        except Exception as e:
            return Response({"estado": "error", "mensaje": f"debe adjuntar una foto {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validar que la foto sea en formato jpg o png
        if request.FILES["foto"].content_type in ["image/jpeg", "image/png"]:
            try:
                fs.save(f"recetas/{foto}", request.FILES['foto'])
                fs.url(request.FILES['foto'])
                # Actualizar la receta con la nueva foto
                Receta.objects.filter(id=request.data["id"]).update(foto=foto)
                #una vez que se actualiza la foto se elimina la anterior foto
                os.remove(f"./uploads/recetas/{anterior}")
                #se retorna un mennsaje de exito
                return Response({"estado": "ok", "mensaje": "La receta se actualizó correctamente"},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"estado": "error", "mensaje": f"Se produjo un error al subir el archivo: {str(e)}"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"estado": "error", "mensaje": "La foto debe ser en formato jpg o png"},
                            status=status.HTTP_400_BAD_REQUEST)
            
            
"""Esta clase es para obtener todos los datos de una receta
por medio deel slug, este codigo se copio de la Clase2 de recetas""" 
            
class Clase2(APIView):
    """esta funcion lleva como parametro el slug
    de la receta y devuelve los datos de esta"""
    def get(self, request, slug):
        try:
            # Consulta los objetos receta por el slug 
            data = Receta.objects.filter(slug=slug).get()
            
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
                }
            }, status=status.HTTP_200_OK)
        except Receta.DoesNotExist:
            return Response({"estado": "error", "mensaje": "la receta no existe"},
                    status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Maneja cualquier error de servidor
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
    """"clase para mostrar las ultimas tres recetas, o de forma random
    no se usa el decoraddor
    ya que no es necesario que el usuario este logueado """    
        
class Clase3(APIView):
    
    def get(self, request):
        """el truco para listar en formato random es usar order_by('?')
        hara algo ssi como select * from recetas ordedr_by random()
        se puede establecer un limite de registros colocando limit 3, ejemplo"""
        data = Receta.objects.order_by('-id').all()[:3]
        datos_json = RecetaSerializer(data, many=True)
        return Response({"data": datos_json.data}, status=status.HTTP_200_OK)
    """El resultado es la lista random de las tres recetas 
    si no se quiere de forma random se le cambia ('?') por ('-id')"""
        
    
        

            
            
            
    
    
class Clase4(APIView):
    
    @logueado() 
    def get(self, request, id):
        #validar que el id del usuario existe
        try:
            usuario_existe = User.objects.get(pk=id)#omito el uso de filter, solo uso get(pk=id) 
        except User.DoesNotExist:
            return Response({"estado": "error", "mensaje": "ocurrio un error en la consulta"},
            status=HTTPStatus.BAD_REQUEST) 
            ##se obtiene el id del usuario logueado validando que exista
        data = Receta.objects.filter(user_id=id).order_by('-id').all()
        #se crea una variable serializer para los datos de la receta      
        datos_json = RecetaSerializer(data, many=True)
        return Response({"data":datos_json.data },status=status.HTTP_200_OK)
    
    
    
    
                        
        
        
        
                    
            
            
            
    
    