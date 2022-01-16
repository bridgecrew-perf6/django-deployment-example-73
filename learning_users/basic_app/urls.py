from django.urls import path
from basic_App import views

app_name = 'basic_App'

urlpatterns = [       
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
]

