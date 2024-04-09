# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django_countries.fields import CountryField
from .models import CustomUser, UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')])
    city = forms.CharField(max_length=30)
    country = CountryField().formfield()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'gender', 'city', 'country']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.gender = self.cleaned_data['gender']
        user.city = self.cleaned_data['city']
        user.country = self.cleaned_data['country']
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'