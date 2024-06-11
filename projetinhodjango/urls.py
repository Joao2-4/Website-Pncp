from django.urls import path
from . import views

urlpatterns = [
    path('', views.consulta_view, name='home'),  # Defina a view para a URL raiz
    path('pub', views.pub , name='pub'),  # Defina a view para a URL raiz
    path('proposta', views.proposta , name='proposta'),
    path('final', views.ultimo , name='final')

]
