

from django.contrib import admin
from django.urls import path
from django.urls import include
#esta importacion es para poder subir archivos en el navegador
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('home.urls')),#ruta base de home
    path('api/v1/',include('ejemplo.urls')),#ruta base de ejemplo
    path('api/v1/',include('categorias.urls')),#la ruta base de categorias
    path('api/v1/',include('recetas.urls')),#la ruta de recetas nueva app
    
]

#estos son los archivos que se encuentran en el settings.py, 
# los estamos importando para que se puedan subir archivos multimedia
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






