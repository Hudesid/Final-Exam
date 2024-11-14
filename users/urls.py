from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('sign/up/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('my/profile/<str:username>/', views.MyProfileDetailView.as_view(), name='my_profile'),
    path('update/profile/<str:username>/', views.UpdateUserProfileView.as_view(), name='update_profile'),
    path('user/profile/<str:username>/', views.UserDetailView.as_view(), name='user_profile'),
    path('verify/email/<int:id>/<str:token>/', views.VerifyEmail.as_view(), name='verify_email'),
]