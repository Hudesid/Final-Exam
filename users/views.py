from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import FormView
from .forms import RegisterForm, LoginForm, User
from blog.models import UserProfile
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
        if profile_image:
            user_profile.profile_image = profile_image
            user_profile.save()
        message = "Sizning emailgizdan Blog Site dan ro'yxatdan o'tildi "
        send_mail(
            'Blog Site dan habar',
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
        user_authenticate = authenticate(self.request, username=username, password=password)
        if user_authenticate is not None:
            login(self.request, user_authenticate)

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
