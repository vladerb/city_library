from django.contrib import admin
from .models import Author, Category, Book, Rating, Comments

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'bio', 'photo']
    search_fields = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created', 'updated']
    list_filter = ['title', 'author', 'category']
    search_fields = ['title', 'author__name']
    raw_id_fields = ['author', 'category']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'score', 'created_at']
    list_filter = ['book', 'user']
    search_fields = ['book__title', 'user__username']

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'created_at']
    list_filter = ['book', 'user']
    search_fields = ['book__title', 'user__username', 'body']
