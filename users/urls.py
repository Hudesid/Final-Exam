from django.urls import path
from .views import Signup, Login, VerifyEmail

app_name = 'users'

urlpatterns = [
    path('sign/up/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('verify/email/<int:id>/<str:token>/', VerifyEmail.as_view(), name='verify_email'),
]