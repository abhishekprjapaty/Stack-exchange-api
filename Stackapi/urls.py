from django.urls import re_path as url, include
 
urlpatterns = [ 
    url(r'^', include('stackapp.urls')), 
]