from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import PostForm, Post, CommentForm, Comment
from users.models import Notification, UserProfile
from users.views import BaseView
from django.contrib.auth.mixins import LoginRequiredMixin


class PostCreateView(BaseView, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create-post.html'
    success_url = reverse_lazy('blog:all_posts')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = get_object_or_404(UserProfile, user=self.request.user)
        post.save()
        form.instance.user = get_object_or_404(UserProfile, user=self.request.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class PostListAll(BaseView, ListView):
    model = Post
    template_name = 'all-posts.html'
    context_object_name = 'posts'


class FollowedListView(BaseView, ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        following = user_profile.following.all()
        return Post.objects.filter(user__in=following).select_related('user').order_by('-created_at')


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
                                 created_at__year=year,
                                 created_at__month=month,
                                 created_at__day=day,
                                 slug=slug
                                 )


    def post(self, *args, **kwargs):
        action = self.request.POST.get('action')
        if action != 'delete-post':
            form = CommentForm(self.request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = self.get_object()
                comment.name =  self.request.user.username
                comment.email = self.request.user.email
                comment.save()
                Notification.objects.create(user=self.get_object().user.user, message=comment.post.title)
                return redirect('blog:post_detail', self.kwargs['year'], self.kwargs['month'], self.kwargs['day'], self.kwargs['slug'])

        return super().post(*args, **kwargs)

class UpdatePostView(BaseView, UpdateView):
    model = Post
    template_name = 'edit-post.html'
    form_class = PostForm

    def get_object(self, queryset=None):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        slug = self.kwargs.get('slug')
        return get_object_or_404(Post,
                                 created_at__year=year,
                                 created_at__month=month,
                                 created_at__day=day,
                                 slug=slug
                                 )

    def get_success_url(self):
        return redirect('users:my_profile', username=self.request.user.username)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['url'] = self.get_object().get_absolute_url('post_detail')
        return context

    def form_invalid(self, form):
        return super().form_invalid(form)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post

    def get_object(self, queryset=None):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        slug = self.kwargs.get('slug')
        return get_object_or_404(Post,
                                 created_at__year=year,
                                 created_at__month=month,
                                 created_at__day=day,
                                 slug=slug
                                 )

    def get_success_url(self):
        return redirect('users:my_profile', username=self.request.user.username)

class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, pk=self.kwargs['pk'])

    def get_success_url(self):
        post = self.get_object().post
        return post.get_absolute_url('post_detail')



class IndexWithoutLogin(View):
    template_name = 'index_without_login.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'index-without-login.html')


