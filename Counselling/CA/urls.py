from .views import *
from django.urls import path
from .import views


urlpatterns = [
    path('', ca_login, name='ca_login'),
    path('c_login',c_login,name='c_login'),
    path('s_login',s_login,name='s_login'),
    path('marks',marks,name='marks'),
    path('attendance',attendance,name='attendance'),
     path('analysis',analysis,name='analysis'),
     path('send_notification',views.send_notification,name='send_notification'),
    
]