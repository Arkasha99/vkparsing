from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/',views.friends, name='users'),
    url(r'^accounts', include('allauth.urls')),
    path('users/logout/',views.log_out,name='logout'),
]