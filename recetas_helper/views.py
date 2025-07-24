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
from django.db.models import Q #para realizar consultas mas complejas  
from categorias.models import Categoria 


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
                    "user_id": data.user_id, 
                    "user":data.user.first_name
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
    ya que no es necesario que el usuario este logueado 
    ests Url es recetas-home """    
        
class Clase3(APIView):
    
    def get(self, request):
        """el truco para listar en formato random es usar order_by('?')
        hara algo si como select * from recetas ordedr_by random()
        se puede establecer un limite de registros colocando limit 3, ejemplo"""
        
        data = Receta.objects.order_by('-id').all()[:3]
        #datos_json se llamaba la variable 
        serializador = RecetaSerializer(data, many=True)
        
        return Response({"data": serializador.data}, status=status.HTTP_200_OK)
    
    """El resultado es la lista random de las tres recetas 
    si no se quiere de forma random se le cambia ('?') por ('-id')"""
        
    
        

            
            
            
"""Esta clase es para validar la existencia del id de usuario
y obtner la recetas por cada usuario logueado protegido
ruta:http://127.0.0.1:8000/api/v1/recetas_panel/id
para acceder se genera el token en loguin con cualquier usuario
y luego se le pasa para listar y ver cuantas recetas creadas tiene el usuario
"""    
    
class Clase4(APIView):
    
    @logueado() 
    def get(self, request, id):
        #validar que el id del usuario existe
        try:
            #usuario_existe = 
            User.objects.get(pk=id)#omito el uso de filter, solo uso get(pk=id) 
        except User.DoesNotExist:
            return Response({"estado": "error", "mensaje": "ocurrio un error en la consulta"},
            status=HTTPStatus.BAD_REQUEST) 
            ##lista las recetas por el id ordenadas de ultimo a primero
            #lista por un usuario en particular
        data = Receta.objects.filter(user_id=id).order_by('-id').all()
        
        #se crea una variable llamada serializador para los datos de la receta 
        serializador = RecetaSerializer(data, many=True)
        
        return Response({"data":serializador.data },status=status.HTTP_200_OK)
        
    
    
    
    
    
    
    """Esta clase es para buscar por categoria_id y por search
    http://127.0.0.1:8000/api/v1/recetas-buscador?categoria_id=4&search=algo""" 
    
    
class Clase5(APIView):
    
    def get(self, request):
        
        #validacion con el parametro categoria_id 
        if request.GET.get("categoria_id") == None or not request.GET.get("categoria_id"):
            
            return Response(
                {"estado":"error", "mensaje": "el campo categoria_id es necesario"},
                status=status.HTTP_400_BAD_REQUEST)
            
            #validamos si la categoria existe o no
        try:
            existe = Categoria.objects.filter(id=request.GET.get("categoria_id")).get()
        except Categoria.DoesNotExist:
            return Response(
                {"estado":"error", "mensaje":"la categorias no se encuentra en la base de datos"
                }, status=status.HTTP_404_NOT_FOUND)
        
        """seria de esta forma en mysql: select * from recetas where categoria_id =6 and nombre
        like '%algo'"""
        """por medio de querystring se obtiene el primer filtro que es el categoria_id"""
        
        data = Receta.objects.filter(
            categoria_id=request.GET.get("categoria_id")
        ).filter(
            nombre__icontains=request.GET.get("search")#otro filtro para buscar por search, con nombre__icontains
        ).order_by('-id').all()
        datos_json = RecetaSerializer(data, many=True,context={'request': request})
        return Response({"data": datos_json.data}, status=status.HTTP_200_OK)
        
    
    
    
    """Otra forma de hacer el bloque de codigo usando Q:
    para consultas mas complejas 
    
    from django.db.models import Q

class Clase5(APIView):
    def get(self, request):
        categoria_id = request.GET.get("categoria_id")
        #si search no se envia toma por defecto un string vacio 
        search = request.GET.get("search", "")

        # Construye el filtro dinámico
        filtros = Q()
        if categoria_id:
            filtros &= Q(categoria_id=categoria_id)
        if search:
            filtros &= Q(nombre__icontains=search) | Q(categoria__nombre__icontains=search)

        data = Receta.objects.filter(filtros).order_by('-id').all()
        datos_json = RecetaSerializer(data, many=True, context={'request': request})
        return Response({"data": datos_json.data}, status=status.HTTP_200_OK)"""
        
        
        
        
        
        
        
    
    
    
    
    
    
                        
        
        
        
                    
            
            
            
    
    