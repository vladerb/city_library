from django.urls import path
from . import views

app_name = 'archive'

urlpatterns = [
    path('', views.BookListView.as_view(), name='books-list'),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name='book-detail'),
    path("books/<int:pk>/rate", views.RateBookView.as_view(), name='rate-book'),
    path("books/<int:pk>/order", views.BookOrderView.as_view(), name='order-book'),
    path('books/<int:pk>/return/', views.BookReturnView.as_view(), name='return-book'),

    path('available/', views.AvailableBookListView.as_view(), name='books-list-available'),

    path("search/", views.BookSearchListView.as_view(), name='search-posts'),

    path('category/<int:pk>', views.CategoryListView.as_view() , name='books-list-category'),

    
]