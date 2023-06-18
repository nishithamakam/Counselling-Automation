from .views import *
from django.urls import path

urlpatterns = [
    path('', ca_login, name='ca_login'),
    path('c_login',c_login,name='c_login'),
    path('s_login',s_login,name='s_login'),
    path('marks',marks,name='marks'),
    path('attendance',attendance,name='attendance'),
     path('analysis',analysis,name='analysis'),
    
]