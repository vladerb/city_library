from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Q
from django.forms import ValidationError
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import RatingForm
from .models import Book, Category, Rating
from accounts.models import BookReceipt

PAGINATION_NUMBER = 9


# Rating
class RateBookView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, pk: int):
        book = get_object_or_404(Book, pk=pk)
        form = RatingForm(request.POST)

        if form.is_valid():
            score = int(form.cleaned_data['score'])
            _, created = Rating.objects.update_or_create(
                book=book,
                user=request.user,
                defaults={'score': score}
            )
            if created:
                messages.success(request, 'Ваш рейтинг був успішно збережений!')
            else:
                messages.info(request, 'Ваш рейтинг був оновлений!')
        else:  
            messages.error(request, 'Виникла помилка при збереженні рейтингу. Будь ласка, спробуйте ще раз.')

        return redirect('archive:book-detail', pk=book.pk)
    

# Category
class CategoryListView(ListView):
    model = Book
    template_name = 'archive/book/book_list.html'
    paginate_by = PAGINATION_NUMBER
    
    context_object_name = 'books'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        return (Book.objects.filter(category=self.category)
                    .select_related('category', 'author')
                    .prefetch_related('receipts')
                    .annotate(average_rating=Avg('rating__score'))
                    )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = self.category
        return context
    

# Books 
class BookListView(ListView):
    model = Book
    template_name = 'archive/book/book_list.html'
    paginate_by = PAGINATION_NUMBER
    
    context_object_name = 'books'
    
    def get_queryset(self):
        return (Book.objects.all()
                .select_related('category', 'author')
                .prefetch_related('receipts')
                .annotate(average_rating=Avg('rating__score'))
                )
    

class AvailableBookListView(ListView):
    model = Book
    template_name = 'archive/book/book_list.html'
    paginate_by = PAGINATION_NUMBER
    
    context_object_name = 'books'
    
    def get_queryset(self):
        return (Book.objects.filter(receipts__isnull=True)
                .select_related('category', 'author')
                .prefetch_related('receipts')
                .annotate(average_rating=Avg('rating__score'))
                )
    

class BookDetailView(DetailView):
    model = Book
    template_name = 'archive/book/book_detail.html'
    context_object_name = 'book'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RatingForm()
        
        if self.request.user.is_authenticated:
            context['has_receipt'] = self.object.receipts.filter(profile=self.request.user.profile).exists() #type: ignore
        else: 
            context['has_receipt'] = False
        return context
    
    def get_queryset(self):
        return (Book.objects
                .select_related('category', 'author')
                .prefetch_related('receipts')
                .annotate(average_rating=Avg('rating__score'))
                )
    

class BookSearchListView(ListView):
    model = Book
    template_name = 'archive/book/book_list.html'
    paginate_by = PAGINATION_NUMBER
    
    context_object_name = 'books'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return (Book.objects
                .filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(author__name__icontains=query))
                .distinct()
                .select_related('category', 'author')
                .prefetch_related('receipts')
                .annotate(average_rating=Avg('rating__score')))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context
    

class BookOrderView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        profile = request.user.profile
        
        try:
            receipt = BookReceipt.objects.create(profile=profile, book=book)
            messages.success(request, f'You have successfully reserved "{book.title}".')
        except ValidationError as e:
            messages.error(request, str(e))

        return redirect('archive:book-detail', pk=book.pk)  
    

class BookReturnView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        receipt = BookReceipt.objects.get(book=book, profile=request.user.profile)
        receipt.delete()
        messages.success(request, 'Книгу успішно повернуто!')

        return redirect('archive:book-detail', pk=book.pk)