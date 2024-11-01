from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.views.generic import FormView
from .forms import RegisterForm, LoginForm, User
from blog.models import UserProfile

class Signup(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        profile_image = form.cleaned_data.get('profile_image')
        user_profile = UserProfile.objects.create(user=user, profile_image=profile_image)
        if profile_image:
            user_profile.profile_image = profile_image
            user_profile.save()
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
