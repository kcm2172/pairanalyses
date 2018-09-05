

from django.contrib import admin
#from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    #url(r'^$', views.home, name='home'),
    # url(r'^$', views.pullData, name='pullData'),
] 
