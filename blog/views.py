from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import PostForm, Post, CommentForm, Comment
from .models import UserProfile, Notification
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin


class BaseView(View):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = get_object_or_404(UserProfile, user=self.request.user)
        context['notifications'] = Notification.objects.filter(user=self.request.user, is_read=False)
        return context

    def post(self, *args, **kwargs):
        action = self.request.POST.get('action')
        if action == 'new follower':
            notification = Notification.objects.filter(user=self.request.user, is_read=False).last()
            if notification:
                notification.is_read = True
                notification.save()
            return redirect('blog:user_profile', username=notification.message)


class PostCreateView(LoginRequiredMixin, BaseView, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create-post.html'
    success_url = reverse_lazy('blog:all_posts')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = get_object_or_404(UserProfile, user=self.request.user)
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
        return Post.objects.filter(user__in=following).select_related('user').order_by('-created_at')


class MyProfileDetailView(LoginRequiredMixin, BaseView, DetailView):
    model = UserProfile
    template_name = 'my-profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, user=self.request.user)

class UserDetailView(LoginRequiredMixin, BaseView, DetailView):
    model = UserProfile
    template_name = 'user-profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        username = self.kwargs['username']
        return get_object_or_404(UserProfile, user__username=username)

    def post(self, *args, **kwargs):
        action = self.request.POST.get('action')
        if action == 'follow':
            self.request.user.userprofile.following.add(self.get_object())
            Notification.objects.create(user=self.get_object().user, message=self.request.user.username)

        elif action == 'unfollow':
            self.request.user.userprofile.following.remove(self.get_object())

        return redirect('blog:user_profile', username=self.get_object())


    def get_context_data(self, *args, **kwargs):
        comments = []
        for post in self.get_object().posts:
            comments.append(post.comments)
        context = super().get_context_data(*args, **kwargs)
        context['follow'] = self.request.user.userprofile.is_following(self.get_object())
        return context

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
        form = CommentForm(self.request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.get_object()
            comment.name =  self.request.user.username
            comment.email = self.request.user.email
            comment.save()
            return redirect('blog:post_detail', self.kwargs['year'], self.kwargs['month'], self.kwargs['day'], self.kwargs['slug'])

class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('users:login')

class UpdatePostView(LoginRequiredMixin, BaseView, UpdateView):
    model = Post
    template_name = 'edit-post.html'
    form_class = PostForm
    success_url = reverse_lazy('blog:index')

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

    def form_invalid(self, form):
        return super().form_invalid(form)

class PostDeleteView(LoginRequiredMixin, BaseView, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')

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

class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment


    def get_object(self, queryset=None):
        return get_object_or_404(Comment, pk=self.kwargs['pk'])

    def get_success_url(self):
        post = self.get_object().post
        return post.get_absolute_url()

class UpdateUserProfileView(LoginRequiredMixin, BaseView, UpdateView):
    model = UserProfile
    template_name = 'edit-profile.html'
    form_class = PostForm
    success_url = reverse_lazy('blog:my_profile')

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, user=self.request.user)


    def form_valid(self, form):
        user = form.save()
        profile_image = form.cleaned_data.get('profile_image')
        user_profile = UserProfile.objects.create(user=user, profile_image=profile_image)
        if profile_image:
            user_profile.profile_image = profile_image
            user_profile.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


