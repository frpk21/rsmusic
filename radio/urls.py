from django.urls import include, path
from radio import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

 
urlpatterns = [
    path('listord/', views.RadicarList.as_view(), name='lista_radicaciones'),
    path('rad/new', views.RadicaForm.as_view(), name='radicaciones'),
    path('rad/edit/<int:pk>', views.RadicarEdit.as_view(), name='rad_edit'),
    path('vendedor/', views.get_ajaxVendedor, name='vendedor_select2'),
    path('rsmusic/', views.RsmusicList.as_view(), name='rsmusic_list'),
    path('rsmusic/new', views.RsmusicNew.as_view(), name='rsmusic_new'),
    path('generos/', views.get_ajaxGenero, name='genero_select2'),
    #path('monitoreo/<int:pk>', views.CreaOrdenView, name='crea_orden'),

]