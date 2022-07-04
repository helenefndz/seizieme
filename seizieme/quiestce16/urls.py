

from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    
    # path('reponse/', views.reponse, name='reponse'),
    # path('verdict/', views.verdict, name='verdict'),
    path('verdict/', views.verdict, name='verdict'),
    ]


