from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, View, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import PostForm, Post, CommentForm, Comment
from .models import UserProfile
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin


class BaseView(View):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = get_object_or_404(UserProfile, user=self.request.user)
        return context


class PostCreateView(LoginRequiredMixin, BaseView, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create-post.html'
    success_url = reverse_lazy('blog:all_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class PostListAll(BaseView, ListView):
    model = Post
    template_name = 'all-posts.html'
    context_object_name = 'posts'


class FollowedListView(LoginRequiredMixin, BaseView, ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        following = user_profile.following.all()
        return Post.objects.filter(user__in=following).select_related('user').order_by('-create_at')


class UserDetailView(LoginRequiredMixin, BaseView, DetailView):
    model = UserProfile
    template_name = 'my-profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, user=self.request.user)

class PostDetailView(BaseView, DetailView):
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


    def post2(self, request):
        form = CommentForm(self.request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.name =  request.user.username
            comment.email = request.user.email
            comment.save()
            return reverse('blog:post_detail', self.kwargs['year'], self.kwargs['month'], self.kwargs['day'], self.kwargs['slug'])

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('users:login')
