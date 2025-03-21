from rest_framework.views import APIView
from django.http import HttpResponse,JsonResponse,Http404
#from django.http import JsonResponse
from rest_framework.response import Response
from http import HTTPStatus
#upload
from django.core.files.storage import FileSystemStorage
import os
from datetime import datetime, timedelta




# para los metodos que no reciben parametros en url se crea una clase
#y para los metodos que reciben parametros se crea otra clase

class Class_Ejemplo(APIView):
    
    #este metodo get no tiene cuerpo de solicitud por lo que no recibe datos json
    def get(self, request):
        #return HttpResponse(f"Esta es una salida get| id={request.GET.get('id', None)} | slug={request.GET.get('slug', None)}")
        #return  Response({'estado':'ok','mensaje':f"Esta es una salida get| id={request.GET.get('id', None)} | slug={request.GET.get('slug', None)}"})
        return Response({'estado':'ok','mensaje':f"Esta es una salida get| id={request.GET.get('id', None)} | slug={request.GET.get
                        ('slug', None)}"},status=HTTPStatus.OK)
        
    
        #este retorna un json con el mensaje que es la forma correcta 
        #en el valor del dict se puede pedir por medio de la request punto "DATA" punto get y el contexto o parametro es 
        #el nombre del campo que es correo y en el pasword es lo mismo, la separacion es por la barra no por comas
    def post(self, request):
        if request.data.get('correo') == None or request.data.get('pasword') == None:
            raise Http404#retorna el mensaje de error en caso que no haya datos
        #return HttpResponse('Esta es una salida post de Rest framework')
        return JsonResponse({"estado":"ok", "mensaje":f"Metodo POST| correo={request.data.get('correo')}| pasword={request.data.get
                            ('pasword')}"}, status=HTTPStatus.CREATED)
        
        
    
    
    def put(self, request):
        #return HttpResponse('Esta es una salida put de Rest framework')
        pass
    
    def delete(self, request):
        return HttpResponse('Esta es una salida delete de Rest framework')
    
    
    
class Class_Ejemplo_Parametros(APIView):
    #estos metodos reciben un argumento que se pasa por la url
    
    def get(self, request, id):
        #return HttpResponse(f"Esta es una salida get de Rest framework'| parametro={id}")
        return JsonResponse({"estado":"confirmado", "mensaje":f"Metodo GET| parametro= {id}"}, status=HTTPStatus.OK)#200
    
    
    
    def post(self, request, id):
        #return HttpResponse(f"Esta es una salida put de Rest framework'| parametro={id}")
        return JsonResponse({
    "estado": "confirmado",
    "mensaje": f"Metodo POST| name={request.data.get('name')} | lastname={request.data.get('lastname')}"
}, status=HTTPStatus.CREATED)
        
        
        
        
    """def post(self, request, id):
        #return JsonResponse({"estado":"confirmado", "mensaje":f"Metodo POST |id={id}"}, status=HTTPStatus.CREATED)
        #return HttpResponse(f"Esta es una salida post de Rest framework'| parametro={id}")
        return JsonResponse({
    "estado": "confirmado",
    "mensaje": f"Metodo POST| name={request.data.get('name')} | lastname={request.data.get('lastname')}"
}, status=HTTPStatus.CREATED)"""

        
        
    def put(self, request, id):
        #return HttpResponse(f"Esta es una salida put de Rest framework'| parametro={id}")
        return JsonResponse({
            "estado":"confirmado",
            "mensaje":f"Metodo put |name={request.data.get('name')},lastname={request.data.get('lastname')}"
            }, status=HTTPStatus.OK)


        
                            

    def delete(self, request, id):
        #return HttpResponse(f"Esta es una salida delete de Rest framework'| parametro={id}")
        return JsonResponse({
            "estado":"confirmado",
            "mensaje":f"Metodo delete |id={id} Elemento eliminado correctamente"
            }, status=HTTPStatus.OK)
        
        
#la clase upload es de ejemplo para subir archivos por 
#lo tanto debe ser post y no recibe parametros por url        
"""class Class_EjemploUpload(APIView):
    def post(self, request):
        #crea una instancia de FileSystemStorage
        fs = FileSystemStorage()
        # Obtener la fecha y hora actual como timestamp
        fecha = datetime.now()
        # mediante datetime se obtiene la fecha y hora actual y se convierte a timestamp
        #asi se evita estar colocando el tipo de archivo que se sube
        foto = f"{datetime.timestamp(fecha)}{os.path.splitext(str(request.FILES['file']))[1]}"
        #guarda el archivo en la carpeta ejemplo con la informacion de la variable foto, esta tiene la fecha
        fs.save(f"ejemplo/{foto}",request.FILES['file'])
        #retorna la url del archivo y hace el guardado de forma completa
        fs.url(request.FILES['file'])
        #retorna un json con el mensaje de que el archivo se subio correctamente
        return JsonResponse({"estado":"ok","mensaje":"archivo subido correctamente"})"""
    
#otra forma de realizar la subida es:
"""from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from datetime import datetime
import os"""

class Class_EjemploUpload(APIView):
    def post(self, request):
        try:
            # Verificar si el archivo está presente en la solicitud
            if 'file' not in request.FILES:
                return JsonResponse({"estado": "error", "mensaje": "No se encontró ningún archivo en la solicitud"}, status=400)

            # Crear una instancia de FileSystemStorage
            fs = FileSystemStorage()

            # Obtener la fecha y hora actual como timestamp
            fecha = datetime.now()
            # Convertir a entero para evitar decimales
            timestamp = int(datetime.timestamp(fecha)) 
            # Obtener la extensión del archivo subido
            file = request.FILES['file']

            extension = os.path.splitext(file.name)[1]

            # Crear un nombre único para el archivo, que contiene fecha y extension
            foto = f"{timestamp}{extension}"

            # Guardar el archivo en la carpeta "ejemplo/"
            file_path = fs.save(f"ejemplo/{foto}", file)
 
            # Obtener la URL del archivo guardado
            file_url = fs.url(file_path)

            # Retornar respuesta exitosa con la URL del archivo
            return JsonResponse({"estado": "ok", "mensaje": "Archivo subido correctamente", "url": file_url})

        except Exception as e:
            # Manejo de excepciones generales
            return JsonResponse({"estado": "error", "mensaje": f"Error al subir el archivo: {str(e)}"}, status=500)
        
        

    
    
        
    
        
    
        
    
    
        
        
    
    