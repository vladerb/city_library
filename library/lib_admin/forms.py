from django import forms
from archive.models import Author, Category, Book


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'photo', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write a short bio about the author...'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Author.objects.filter(name=name).exists():
            raise forms.ValidationError('An author with this name already exists.')
        return name
    

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Category.objects.filter(title=title).exists():
            raise forms.ValidationError('A category with this title already exists.')
        return title
    

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['author', 'title', 'category', 'cover', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter the book description...'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Book.objects.filter(title=title).exists():
            raise forms.ValidationError('A book with this title already exists.')
        return title
