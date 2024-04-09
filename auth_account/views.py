from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView, UpdateView
from django.contrib.auth.models import User  # Import User model
from .models import CustomUser, UserProfile
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm

class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'auth/registration.html'
    success_url = reverse_lazy('accountAuth:login')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        
        # Check if the username or email already exists
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(self.request, 'Username or email already exists.')
            return self.form_invalid(form)
        
        response = super().form_valid(form)
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        if user:
            login(self.request, user)
        return response


class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = 'auth/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Check if the username or email and password match
        username_or_email = form.cleaned_data.get('username_or_email')
        password = form.cleaned_data.get('password')

        # Authenticate user
        user = authenticate(username=username_or_email, password=password)
        
        if user is not None:  # If authentication is successful
            login(self.request, user)  # Log in the user
            return super().form_valid(form)  # Proceed with the default form validation
        else:
            # If authentication fails, add an error to the form
            form.add_error(None, 'Invalid username/email or password.')
            return self.form_invalid(form)  # Return invalid form response


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class UserProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'auth/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        # Get or create the user profile object
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

