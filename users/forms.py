from django import forms
from blog.models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )

    password2 = forms.CharField(
        label='Password(again)',
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )

    profile_image = forms.ImageField(
        label='Avatar',
        required=False,
        widget=forms.FileInput(attrs={'class':'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'})
        }



class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        label='Name',
        widget=forms.TextInput(attrs={'class':'form-control'})
    ),
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )