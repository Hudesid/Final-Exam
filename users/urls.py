from django.urls import path
from .views import Signup, Login

app_name = 'users'

urlpatterns = [
    path('sign/up/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login')
]