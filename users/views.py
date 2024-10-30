from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import FormView
from .forms import RegisterForm, LoginForm, User
from blog.models import UserProfile

class Signup(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('blog:all_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        profile_image = form.cleaned_data.get('profile_image')
        user_profile = UserProfile.objects.create(user=user)
        if profile_image:
            user_profile.profile_image = profile_image
            user_profile.save()

        return super().form_valid(form)


class Login(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('blog:all_list')

    def form_invalid(self, form):
        cd = form.cleaned_data
        user = authenticate(self.request, username=cd['username'], password=cd['password'])
        if user is not None:
            login(self.request, user)
        else:
            return render(self.request, 'login.html', {'user': user})

        return super().form_invalid(form)

