from django.urls import path
from . import views

app_name = 'lib-admin'

urlpatterns = [
    path('authors/', views.AuthorListView.as_view(), name='authors-list'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('authors/<int:pk>/edit', views.AuthorEditView.as_view(), name='author-edit'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),

    path('category/', views.CategoryListView.as_view(), name='categories-list'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('category/<int:pk>/edit', views.CategoryEditView.as_view(), name='category-edit'),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),

    path('books/', views.BookListView.as_view(), name='books-list'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/edit', views.BookEditView.as_view(), name='book-edit'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),

    path('books-receipts/', views.BookReceiptListView.as_view(), name='books-receipts-list'),
    path('books-receipts/create/', views.BookReceiptCreateView.as_view(), name='book-receipts-create'),
    path('books-receipts/<int:pk>/edit', views.BookReceiptEditView.as_view(), name='book-receipts-edit'),
    path('books-receipts/<int:pk>/delete/', views.BookReceiptDeleteView.as_view(), name='book-receipts-delete'),

    path('users/', views.UserListView.as_view(), name='users-list'),
    path('users/<int:pk>/edit', views.UserProfileEditView.as_view(), name='user-edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),
]