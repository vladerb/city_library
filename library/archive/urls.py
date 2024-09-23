from django.urls import path
from . import views

app_name = 'archive'

urlpatterns = [
    path('', views.BookListView.as_view(), name='books-list'),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name='book-detail'),
    path("books/<int:pk>/rate", views.RateBookView.as_view(), name='rate-book'),

    path('category/<int:pk>', views.CategoryListView.as_view() , name='books-list-category'),
]