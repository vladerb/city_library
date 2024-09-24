from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView, UpdateView
from django.urls import reverse_lazy

from .forms import UserRegistrationForm, UserEditForm, ProfileEditFrom

# User
class UserRegisterView(SuccessMessageMixin, CreateView):
    model = get_user_model()
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:user-login')
    success_message = "Registration successful! You can now log in."

    def form_valid(self, form):
        response = super().form_valid(form)
        next_url = self.request.POST.get('next')
        if next_url:
            return redirect(next_url)
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)
    
    def get_success_url(self) -> str:
        return super().get_success_url()
    
    
class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = False
    

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['books'] = (user.profile.books_received # type: ignore
                            .select_related('category', 'author') 
                            .annotate(average_rating=Avg('rating__score'))  
                            .all())
        return context


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserEditForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:user-profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['profile_form'] = ProfileEditFrom(data=self.request.POST, files=self.request.FILES, instance=self.request.user.profile) # type: ignore
        else:
            context['profile_form'] = ProfileEditFrom(instance=self.request.user.profile) #type: ignore
        return context

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Profile updated successfully.')
        return response

# Password
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:user-profile')

    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully.')
        return super().form_valid(form)

