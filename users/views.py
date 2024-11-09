from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.views.generic import FormView, View
from .forms import RegisterForm, LoginForm, User
from blog.models import UserProfile, UserToken
from django.conf import settings

class Signup(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        email = form.cleaned_data['email']
        profile_image = form.cleaned_data.get('profile_image')
        user_profile = UserProfile.objects.create(user=user, profile_image=profile_image)
        user_token = UserToken.create(user_profile=user)
        token = user_token.token
        verification_link = reverse('users:verify_email', args=[user_profile.user.id, token])
        current_site = get_current_site(self.request)
        full_link = f"http://{current_site.domain}{verification_link}"
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

class VerifyEmail(View):
    def get(self, request, id, token, *args, **kwargs):
        user_profile = UserProfile.objects.get(pk=id)
        user_token = UserToken.objects.get(user_profile=user_profile, token=token)
        user_profile.is_verified_email = True
        user_profile.save()
        return redirect('app_name:login')