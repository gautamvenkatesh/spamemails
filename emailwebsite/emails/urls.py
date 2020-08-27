from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^ajax/emailupdate/$', views.emails, name='emailupdate'),
    url(r'^ajax/emaildelete/$', views.delete, name = 'emaildelete')
]