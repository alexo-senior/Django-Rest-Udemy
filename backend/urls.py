

from django.contrib import admin
from django.urls import path
from django.urls import include
from seguridad import urls as seguridad_urls  # Import the seguridad.urls module
#esta importacion es para poder subir archivos en el navegador
from django.conf import settings
from django.conf.urls.static import static
from recetas_helper import urls as recetas_helper_urls  # Import the recetas_helper.urls module






urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('home.urls')),#ruta base de home
    path('api/v1/',include('ejemplo.urls')),#ruta base de ejemplo
    path('api/v1/',include('categorias.urls')),#la ruta base de categorias
    path('api/v1/',include('recetas.urls')),#la ruta de recetas nueva app recetas
    path('api/v1/', include(seguridad_urls)),
    path('api/v1/', include(recetas_helper_urls)),  # Import the recetas_helper.urls module
    
]

#estos son los archivos que se encuentran en el settings.py, 
# los estamos importando para que se puedan subir archivos multimedia
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)








