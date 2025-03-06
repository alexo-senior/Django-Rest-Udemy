

from django.contrib import admin
from django.urls import path
from django.urls import include
#esta importacion es para poder subir archivos en el navegador
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('home.urls')),
    path('api/v1/',include('ejemplo.urls')),
]

#estos son los archivos que se encuentran en el settings.py, 
# los estamos importando para que se puedan subir archivos
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






