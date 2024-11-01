from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.FollowedListView.as_view(), name='index'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('all/post/', views.PostListAll.as_view(), name='all_post'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('my/profile/', views.UserDetailView.as_view(), name='my_profile'),
    path('post/detail/<int:year>/<int:month>/<int:day>/<slug:slug>', views.PostDetailView.as_view(), name='post_detail')
]