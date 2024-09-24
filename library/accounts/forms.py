import datetime
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Profile, Contact


User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    usable_password = None

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Email is already registered.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3: # type: ignore
            raise forms.ValidationError('Username must be at least 3 characters long.')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists.')
        return username
    
    
class UserEditForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Email is already registered.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3: # type: ignore
            raise forms.ValidationError('Username must be at least 3 characters long.')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Username already exists.')
        return username
    

class ProfileEditFrom(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo', 'place_of_study', 'form_of_study']
        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date',  'placeholder': 'Select your birth date'}
            ),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'place_of_study': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your place of study'}),
            'form_of_study': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth and date_of_birth >= datetime.date.today():
            raise forms.ValidationError('Date of birth must be in the past.')
        return date_of_birth
    

# FeedBack    
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Send Message'))