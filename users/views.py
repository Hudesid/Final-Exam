from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import FormView, View, DetailView
from .forms import RegisterForm, LoginForm, User
from .models import UserProfile, UserToken, Notification
from blog.models import Post
from django.conf import settings

class Signup(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        email = form.cleaned_data['email']
        profile_image = form.cleaned_data.get('profile_image')
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_token = UserToken.objects.create(user_profile=user_profile)
        token = user_token.token
        verification_link = reverse('users:verify_email', args=[user_profile.id, token])
        current_site = get_current_site(self.request)
        full_link = f"https://{current_site}{verification_link}"
        if profile_image:
            user_profile.profile_image = profile_image
        user_profile.save()
        message = f"Sizning emailgizdan Blog Site dan ro'yxatdan o'tildi\\Ushbu link orqali saytga o'tsangiz bo'ladi {full_link}"
        send_mail(
            'Blog Site dan habar',
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
        # user_authenticate = authenticate(self.request, username=username, password=password)
        # if user_authenticate is not None:
        #     login(self.request, user_authenticate)

        return super().form_valid(form)


class Login(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Invalid username or password.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('users:login')

class VerifyEmail(View):
    def get(self, request, id, token, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, pk=id)
        user_token = get_object_or_404(UserToken, user_profile=user_profile, token=token)
        user_profile.is_verified_email = True
        user_profile.save()
        return redirect('users:login')

class BaseView(LoginRequiredMixin, View):

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
            return redirect('users:user_profile', username=notification.message)

        if action == 'new comment':
            notification = Notification.objects.filter(user=self.request.user, is_read=False).last()
            if notification:
                notification.is_read = True
                notification.save()

            post = get_object_or_404(Post, title=notification.message)
            if self.request.path == redirect(post.get_absolute_url('post_detail')):
                return post.get_absolute_url('post_detail')
            return redirect(post.get_absolute_url_2('post_detail'))

        return super().post(*args, **kwargs)

class MyProfileDetailView(BaseView, DetailView):
    model = UserProfile
    template_name = 'my-profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, user=self.request.user)

class UserDetailView(BaseView, DetailView):
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

        return redirect('users:user_profile', username=self.get_object())


    def get_context_data(self, *args, **kwargs):
        comments = []
        for post in self.get_object().posts:
            comments.append(post.comments)
        context = super().get_context_data(*args, **kwargs)
        context['follow'] = self.request.user.userprofile.is_following(self.get_object())
        return context

class UpdateUserProfileView(BaseView, UpdateView):
    model = UserProfile
    template_name = 'edit-profile.html'
    form_class = RegisterForm

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object().user
        return kwargs

    def get_success_url(self):
        return reverse('users:my_profile', kwargs={'username': self.object.user.username})

    def form_valid(self, form):
        user = self.get_object().user
        user_profile = self.get_object()
        password1 = form.cleaned_data.get('password1')
        password2 = form.cleaned_data.get('password2')
        profile_image = form.cleaned_data.get('profile_image')

        if password1 and password2:
            if user.check_password(password1):
                user.set_password(password2)
                update_session_auth_hash(self.request, user)
                messages.success(self.request, 'Your password was successfully updated!')
            else:
                messages.error(self.request, 'Current password is incorrect. Please try again.')
                return self.form_invalid(form)

        user.username = form.cleaned_data.get('username')
        user.email = form.cleaned_data.get('email')

        if profile_image:
            user_profile.profile_image = profile_image

        user.save()
        user_profile.save()
        messages.success(self.request, 'Your profile was successfully updated!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error updating your profile. Please check the form and try again.')
        return super().form_invalid(form)