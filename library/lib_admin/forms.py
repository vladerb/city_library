from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

from archive.models import Author, Category, Book

User = get_user_model()

# Authors
class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'photo', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write a short bio about the author...'}),
        }
    

# Categories
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Category.objects.filter(title=title).exists():
            raise forms.ValidationError('A category with this title already exists.')
        return title
    

# Books
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['author', 'title', 'category', 'cover', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter the book description...'}),
        }


# Users
class UserEditForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff']

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


