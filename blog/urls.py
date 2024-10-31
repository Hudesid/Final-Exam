from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListAll.as_view(), name='all_list'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('index/', views.UserPostList.as_view(), name='index'),
    path('my/profile/', views.UserDetailView.as_view(), name='my_profile'),
    path('post/detail/<int:year>/<int:month>/<int:day>/<slug:slug>', views.PostDetailView.as_view(), name='post_detail')
]