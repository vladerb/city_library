from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Avg
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from accounts.models import BookReceipt
from accounts.forms import ProfileEditForm
from archive.models import Author, Category, Book
from .forms import AuthorForm, CategoryForm, BookForm, UserEditForm, BookReceiptsForm

PAGINATION_NUMBER = 9
USER = get_user_model()


# Mixin
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff # type: ignore
    
    def handle_no_permission(self):
        messages.error(self.request, 'У доступі відмовлено!') # type: ignore
        return redirect(reverse('accounts:user-profile'))


# Authors
class AuthorCreateView(StaffRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'lib_admin/forms/author_create.html'
    success_url = reverse_lazy('lib-admin:authors-list')

class AuthorEditView(StaffRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'lib_admin/forms/author_edit.html'
    success_url = reverse_lazy('lib-admin:authors-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        if not form.cleaned_data['photo']:
            form.instance.photo = 'authors/default_author.png'
        return super().form_valid(form)
    
class AuthorDeleteView(StaffRequiredMixin, DeleteView):
    model = Author
    template_name = 'lib_admin/del/author_confirm_delete.html'
    success_url = reverse_lazy('lib-admin:authors-list') 

class AuthorListView(StaffRequiredMixin, ListView):
    model = Author
    template_name = 'lib_admin/lists/authors_list.html'
    context_object_name = 'authors'
    paginate_by = PAGINATION_NUMBER

    def get_queryset(self):
        sort_field = self.request.GET.get('sort', 'id')
        order = self.request.GET.get('order', 'asc')

        queryset = Author.objects.all()

        if order == 'desc':
            sort_field = '-' + sort_field

        return queryset.order_by(sort_field)


# Categories
class CategoryCreateView(StaffRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'lib_admin/forms/category_create.html'
    success_url = reverse_lazy('lib-admin:categories-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        next_url = self.request.POST.get('next')
        if next_url:
            return redirect(next_url)
        return response
    
class CategoryEditView(StaffRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'lib_admin/forms/category_edit.html'
    success_url = reverse_lazy('lib-admin:categories-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class CategoryDeleteView(StaffRequiredMixin, DeleteView):
    model = Category
    template_name = 'lib_admin/del/category_confirm_delete.html'
    success_url = reverse_lazy('lib-admin:categories-list')

class CategoryListView(StaffRequiredMixin, ListView):
    model = Category
    template_name = 'lib_admin/lists/categories_list.html'
    context_object_name = 'categories'
    paginate_by = PAGINATION_NUMBER

    def get_queryset(self):
        sort_field = self.request.GET.get('sort', 'id')
        order = self.request.GET.get('order', 'asc')

        queryset = Category.objects.all()

        if order == 'desc':
            sort_field = '-' + sort_field

        return queryset.order_by(sort_field)


# Books
class BookCreateView(StaffRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'lib_admin/forms/book_create.html'
    success_url = reverse_lazy('lib-admin:books-list')

class BookEditView(StaffRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'lib_admin/forms/book_edit.html'
    success_url = reverse_lazy('lib-admin:books-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
        if not form.cleaned_data['cover']:
            form.instance.cover = 'books/default_book_cover.png'
        return super().form_valid(form)
    
class BookDeleteView(StaffRequiredMixin, DeleteView):
    model = Book
    template_name = 'lib_admin/del/book_confirm_delete.html'
    success_url = reverse_lazy('lib-admin:books-list')

class BookListView(StaffRequiredMixin, ListView):
    model = Book
    template_name = 'lib_admin/lists/books_list.html'
    context_object_name = 'books'
    paginate_by = PAGINATION_NUMBER

    def get_queryset(self):
        sort_field = self.request.GET.get('sort', 'id')
        order = self.request.GET.get('order', 'asc')

        queryset = (Book.objects.all()
                    .select_related('category', 'author')
                    .prefetch_related('receipts')
                    .annotate(average_rating=Avg('rating__score')))
        
        if order == 'desc':
            sort_field = '-' + sort_field

        return queryset.order_by(sort_field)


# Books Receipts
class BookReceiptCreateView(StaffRequiredMixin, CreateView):
    model = BookReceipt
    form_class = BookReceiptsForm
    template_name = 'lib_admin/forms/book_receipt_create.html'
    success_url = reverse_lazy('lib-admin:books-receipts-list')

class BookReceiptEditView(StaffRequiredMixin, UpdateView):
    model = BookReceipt
    form_class = BookReceiptsForm
    template_name = 'lib_admin/forms/book_receipt_edit.html'
    success_url = reverse_lazy('lib-admin:books-receipts-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    
class BookReceiptDeleteView(StaffRequiredMixin, DeleteView):
    model = BookReceipt
    template_name = 'lib_admin/del/book_receipts_confirm_delete.html'
    success_url = reverse_lazy('lib-admin:books-receipts-list')

class BookReceiptListView(StaffRequiredMixin, ListView):
    model = BookReceipt
    template_name = 'lib_admin/lists/books_receipts_list.html'
    context_object_name = 'receipts'
    paginate_by = PAGINATION_NUMBER

    def get_queryset(self):
        sort_field = self.request.GET.get('sort', 'id')
        order = self.request.GET.get('order', 'asc')
        
        queryset = (BookReceipt.objects.all()
                    .select_related('profile', 'book'))
        
        if order == 'desc':
            sort_field = '-' + sort_field
        
        # Return sorted queryset
        return queryset.order_by(sort_field)



# Users
class UserProfileEditView(StaffRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserEditForm
    template_name = 'lib_admin/forms/user_edit.html'
    success_url = reverse_lazy('lib-admin:users-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['profile_form'] = ProfileEditForm(data=self.request.POST, files=self.request.FILES, instance=self.request.user.profile) # type: ignore
        else:
            context['profile_form'] = ProfileEditForm(instance=self.request.user.profile) #type: ignore
        return context

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('pk') 
        return get_user_model().objects.get(pk=user_id)

    def form_valid(self, form):
        response = super().form_valid(form)
        profile_form = ProfileEditForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)  # type: ignore
        if profile_form.is_valid():
            profile_form.save()
            messages.success(self.request, 'Profile updated successfully.')
        else:
            messages.error(self.request, 'There was an error updating the profile.')

        return response

class UserDeleteView(StaffRequiredMixin, DeleteView):
    model = USER
    template_name = 'lib_admin/del/user_confirm_delete.html'
    success_url = reverse_lazy('lib-admin:users-list')

class UserListView(StaffRequiredMixin, ListView):
    model = USER
    template_name = 'lib_admin/lists/users_list.html'
    context_object_name = 'users'
    paginate_by = PAGINATION_NUMBER

    def get_queryset(self):
        sort_field = self.request.GET.get('sort', 'id')
        order = self.request.GET.get('order', 'asc')

        queryset = (USER.objects.all()
                    .select_related('profile'))
        
        if order == 'desc':
            sort_field = '-' + sort_field

        return queryset.order_by(sort_field)