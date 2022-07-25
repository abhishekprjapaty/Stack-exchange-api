from django.urls import re_path as url
from stackapp import views 
 
urlpatterns = [ 
    url(r'^', views.home),
    url(r'^/search', views.search),
]