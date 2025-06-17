

from django.contrib import admin
from django.urls import path
from django.urls import include
from seguridad import urls as seguridad_urls  # Import the seguridad.urls module
#esta importacion es para poder subir archivos en el navegador
from django.conf import settings
from django.conf.urls.static import static
from recetas_helper import urls as recetas_helper_urls  # Import the recetas_helper.urls module
#para el swagger 
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

#primero se debe configurar la varible de get_schema_view
#dentro de openapi los atributos de title, description, terms_of_service
#contac, y license cada uno con su definicion, esto viene preestablecido
schema_view = get_schema_view(
    openapi.Info(
        title="Curso Fullstack Django + RestFramewor + Vue",
        default_version='v1',
        description="Api desarrollada para implementacion de Backend de sistema de recetas, para curso Fullstack",
        terms_of_service="https://colnodo.org/es/crececongoogle/inscripcion#preguntas/",
        contact=openapi.Contact(email="alexobarrafer@gmail.com"),
        license=openapi.License(name="BSD License")  # el termino BSD license significa licencia libre
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
    




urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('home.urls')),#ruta base de home
    path('api/v1/',include('ejemplo.urls')),#ruta base de ejemplo
    path('api/v1/',include('categorias.urls')),#la ruta base de categorias
    path('api/v1/',include('recetas.urls')),#la ruta de recetas nueva app recetas
    path('api/v1/', include(seguridad_urls)),
    path('api/v1/', include(recetas_helper_urls)),  # Import the recetas_helper.urls module
    #se configura tal cual como dice la documentacion oficial
    path('documentacion<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    #mi url general se llamara solo documentacion
    path('documentacion/', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',cache_timeout=0), name='schema-redoc'),
]

#estos son los archivos que se encuentran en el settings.py, 
# los estamos importando para que se puedan subir archivos multimedia
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)








