from rest_framework.views import APIView
from django.http import HttpResponse,JsonResponse,Http404
#from django.http import JsonResponse
from rest_framework.response import Response
from http import HTTPStatus



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
        
    
    