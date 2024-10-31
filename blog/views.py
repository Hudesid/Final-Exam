from django.shortcuts import render, get_object_or_404, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import PostForm, Post, CommentForm, Comment
from .models import UserProfile
from django.contrib.auth import logout, login


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create-post.html'
    success_url = reverse_lazy('blog:all_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponse('Form is invalid')

class PostListAll(ListView):
    model = Post
    template_name = 'all-posts.html'
    context_object_name = 'posts'

    def post(self, request):
        logout(request)
        return reverse('users:login')

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

class PostDetailView(DetailView):
    model = Post
    template_name = 'show-post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def get_object(self, queryset=None):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        slug = self.kwargs.get('slug')
        return get_object_or_404(Post,
                                 create_at__year=year,
                                 create_at__month=month,
                                 create_at__day=day,
                                 slug=slug
                                 )


    def post(self, request):
        form = CommentForm(self.request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.name =  request.user.username
            comment.email = request.user.email
            comment.save()
            return reverse('blog:post_detail', self.kwargs['year'], self.kwargs['month'], self.kwargs['day'], self.kwargs['slug'])


