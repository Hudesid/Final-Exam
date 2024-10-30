from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import PostForm, Post
from .models import UserProfile


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create-post.html'
    success_url = reverse_lazy('blog:create_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return reverse('blog:create_post')

class PostListAll(ListView):
    model = Post
    template_name = 'all-post.html'
    context_object_name = 'posts'

class UserPostList(ListView):
    model = UserProfile
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = UserProfile.objects.get(user__username=self.kwargs['username'])
        return posts.posts.all()

class UserDetailView(DetailView):
    model = UserProfile
    template_name = 'my-profile'
    context_object_name = 'user'

    def get_queryset(self):
        user = UserProfile.objects.get(user__username=self.kwargs['username'])
        return user

class PostDetail(DetailView):
    model = Post
    template_name = 'show-post.html'


