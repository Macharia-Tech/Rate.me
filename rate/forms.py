from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username=forms.CharField(max_length=30, required=False, help_text='Optional.')
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    Bio=forms.CharField(max_length=70, required=False, help_text='Optional.')
    name=forms.CharField(max_length=30, required=False, help_text='Optional.')
    profile_image=forms.ImageField()
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','Bio','name','profile_image','email', 'password1', 'password2', )
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields=('first_name','last_name','email')


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']










    