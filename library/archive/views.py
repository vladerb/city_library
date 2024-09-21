from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.db.models import Q, Avg
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView


from .models import Book, Category, Rating, Comments
# from .forms import TagFormModel, RatingForm, ContactForm

# Books
class PostListView(ListView):
    model = Book
    template_name = 'archive/book/book_list.html'
    paginate_by = 6
    
    context_object_name = 'books'
    
    def get_queryset(self):
        return (Book.objects.all()
                .select_related('category')
                .annotate(average_rating=Avg('rating__score'))
                )
