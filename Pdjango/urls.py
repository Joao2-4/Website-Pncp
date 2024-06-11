from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projetinhodjango.urls')),  # Adicione esta linha para a URL raiz
]
