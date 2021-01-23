from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from allauth.account.forms import SignupForm


class SelfSignUpForm (SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].label = ""
        self.fields["email"].widget.attrs.update({'class': 'form-control-lg'})

        self.fields["username"].label = ""
        self.fields["username"].widget.attrs.update({'class': 'form-control-lg'})

        self.fields["password1"].label = ''
        self.fields["password1"].widget.attrs.update({'class': 'form-control-lg'})
        
        self.fields["password2"].label = '' 
        self.fields["password2"].widget.attrs.update({'class': 'form-control-lg'})

        # self.fields["email"].label = ""


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class UserUpdateForm(forms.ModelForm):
    #email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'details']

