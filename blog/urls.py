from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.FollowedListView.as_view(), name='index'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('all/post/', views.PostListAll.as_view(), name='all_posts'),
    path('index/without/login/', views.IndexWithoutLogin.as_view(), name='index_without_login'),
    path('delete/comment/<int:pk>/', views.DeleteCommentView.as_view(), name='comment_delete'),
    path('post/detail/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/update/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.UpdatePostView.as_view(), name='post_update'),
    path('post/delete/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.PostDeleteView.as_view(), name='post_delete')
]