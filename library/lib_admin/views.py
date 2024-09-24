from django.urls import reverse_lazy
from django.views.generic import CreateView

from archive.models import Author, Category, Book
from .forms import AuthorForm, CategoryForm, BookForm

class AuthorCreateView(CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'authors/author_form.html'
    success_url = reverse_lazy('authors:author-list')

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('categories:category-list')

class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('books:book-list')
