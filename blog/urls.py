from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.FollowedListView.as_view(), name='index'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('all/post/', views.PostListAll.as_view(), name='all_posts'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('my/profile/<str:username>', views.MyProfileDetailView.as_view(), name='my_profile'),
    path('update/profile/<str:username>', views.UpdateUserProfileView.as_view(), name='update_profile'),
    path('user/profile/<str:username>', views.UserDetailView.as_view(), name='user_profile'),
    path('delete/comment/<int:pk>', views.DeleteCommentView.as_view(), name='comment_delete'),
    path('post/detail/<int:year>/<int:month>/<int:day>/<slug:slug>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/update/<int:year>/<int:month>/<int:day>/<slug:slug>', views.UpdatePostView.as_view(), name='post_update'),
    path('post/delete/<int:year>/<int:month>/<int:day>/<slug:slug>', views.PostDeleteView.as_view(), name='post_delete')
]