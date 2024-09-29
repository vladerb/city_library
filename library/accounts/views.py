from datetime import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView, UpdateView, FormView
from django.urls import reverse_lazy

import logging

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, ContactForm


# Feedback
class FeedbackView(FormView):
    template_name = 'accounts/feedback/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('accounts:feedback-success')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your message has been sent successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error in the form. Please check your inputs.')
        return super().form_invalid(form)


class FeedbackSuccessView(TemplateView):
    template_name = 'accounts/feedback/feedback_success.html'


# User
user_logger = logging.getLogger('user_accounts')

class UserRegisterView(SuccessMessageMixin, CreateView):
    model = get_user_model()
    form_class = UserRegistrationForm
    template_name = 'accounts/user/register.html'
    success_url = reverse_lazy('accounts:user-login')
    success_message = "Registration successful! You can now log in."

    def form_valid(self, form):
        response = super().form_valid(form)
        next_url = self.request.POST.get('next')
        if next_url:
            return redirect(next_url)
        user_logger.info(
            f"[{datetime.now()}] INFO: User registered successful| "
            f"User: {form.cleaned_data['username']} | "
            f"IP: {self.request.META.get('REMOTE_ADDR')}"
        ) 
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        user_logger.warning(
            f"[{datetime.now()}] WARNING: User registered failed| "
            f"IP: {self.request.META.get('REMOTE_ADDR')}"
        ) 
        return super().form_invalid(form)
    
    def get_success_url(self) -> str:
        return super().get_success_url()
    
    
class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "accounts/user/login.html"
    redirect_authenticated_user = False

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        user_logger.info(
            f"[{datetime.now()}] INFO: User log-in successful| "
            f"User: {form.cleaned_data['username']} | "
            f"IP: {self.request.META.get('REMOTE_ADDR')}"
        ) 
        return super().form_valid(form)
    
    def form_invalid(self, form: AuthenticationForm) -> HttpResponse:
        user_logger.warning(
            f"[{datetime.now()}] WARNING: User log-in failed  | "
            f"IP: {self.request.META.get('REMOTE_ADDR')}"
        ) 
        return super().form_invalid(form)
    

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['books'] = (user.profile.books_received # type: ignore
                            .select_related('category', 'author') 
                            .prefetch_related('receipts')
                            .annotate(average_rating=Avg('rating__score'))  
                            .all())
        return context


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserEditForm
    template_name = 'accounts/user/profile_edit.html'
    success_url = reverse_lazy('accounts:user-profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['profile_form'] = ProfileEditForm(data=self.request.POST, files=self.request.FILES, instance=self.request.user.profile) # type: ignore
        else:
            context['profile_form'] = ProfileEditForm(instance=self.request.user.profile) #type: ignore
        return context

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        profile_form = ProfileEditForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)  # type: ignore
        if profile_form.is_valid():
            profile_form.save()
            messages.success(self.request, 'Profile updated successfully.')
        else:
            messages.error(self.request, 'There was an error updating the profile.')

        return response

# Password
pass_logger = logging.getLogger('user_password')

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/user/password_change.html'
    success_url = reverse_lazy('accounts:user-profile')
    
    def form_valid(self, form):
        pass_logger.info(
            f"[{datetime.now()}] INFO: Password change successful | "
            f"User: {self.request.user.username} | " # type: ignore
            f"IP: {self.request.META.get('REMOTE_ADDR')}"
        ) 
        messages.success(self.request, 'Password changed successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        pass_logger.warning(
            f"[{datetime.now()}] WARNING: Password change failed  | "
            f"User: {self.request.user.username} | " # type: ignore
            f"IP: {self.request.META.get('REMOTE_ADDR')}"
        ) 
        return super().form_invalid(form)

