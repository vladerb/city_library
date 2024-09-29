from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg
from django.urls import reverse

User = get_user_model()


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)
    photo = models.ImageField(upload_to='authors/', default='authors/default_author.png', null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name



class Category(models.Model):
    title = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("archive:books-list-category", args=[self.pk])


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(verbose_name="Book`s title", max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books', null=True, blank=True)
    cover = models.ImageField(upload_to='books/', default='books/default_book_cover.png', null=True, blank=True)
    description = models.TextField(verbose_name="Book`s description", default='No description.', max_length=500, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def average_rating(self) -> int:
        return int(round(Rating.objects.filter(book=self).aggregate(Avg('score'))['score__avg'] or 0))
    
    def __str__(self) -> str:
        return f'{self.title} - {self.author}'
    

class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)   
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
class Comments(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
