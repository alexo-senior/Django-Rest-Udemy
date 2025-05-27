from functools import wraps
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from http import HTTPStatus
from jose import jwt
from django.conf import settings 
import time





# el estandar es colocarle el nombre de decorators
#el decorador es una funcion que recibe como parametro otra funcion
# el decorador debe retornar una funcion decorada
# el decorador puede recibir argumentos
def logueado(): #opcional colocarle el parametro de redirect_url=None 
    def metodo(func):
        @wraps(func)
        #este request es del decorador no es de la vista
        #va a recibir argumentos(args) y kwargs 
        def _decorator(request, *args, **kwargs):
            #aqui se agrega la logica que se desea ejecutar antes de la funcion decorada
            #obtienes el request del metodo que decoraste con el decorador 
            req = args[0]
            if not req.headers.get('Authorization') or req.headers.get('Authorization')==None:
                return Response({"estado": "error", "mensaje":" no esta autorizado"}, status=HTTPStatus)
            #debido a que el token tiene dos partes primero se hace el Bearer y luego el token
            #se debe separar el token con el espacio 
            #se crea una variable para obtener los headeers de la peticion
            header = req.headers.get('Authorization').split(' ')
            resuelto = jwt.decode(header[1], settings.SECRET_KEY, algorithms=['HS256'])

            try:
                resuelto = jwt.decode(header[1], settings.SECRET_KEY, algorithms=['HS256'])
                
            except Exception as e:
                return Response({"estado": "error", "mensaje":" no esta autorizado"}, 
                        status=HTTPStatus.UNAUTHORIZED)
            #para validar el token se debe verificar que el token no haya expirado
            # si la fecha es mayor a la fecha actual esta vigente sino es una fecha anterior
            if int(resuelto["exp"]>int(time.time())):
                return func(request, *args, **kwargs)
            else:
                return Response({"estado": "error", "mensaje":" no esta autorizado"}, 
                        status=HTTPStatus.UNAUTHORIZED)
        return _decorator
    return metodo 
            
                
            #si el token es valido se ejecuta la funcion decorada
            
            
            #SI EL TOKEN ES VALIDO
            #como se decodifica el token


# el decorador permite ejecutar una funcionalidad antes de ejecutar la funcion decorada
# en este caso, el decorador logueado se ejecuta antes de la funcion post
@logueado()
def post():
    pass

