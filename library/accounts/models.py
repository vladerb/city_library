from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from datetime import timedelta, datetime

from archive.models import Book

User = get_user_model()


class Profile(models.Model):
    FORM_OF_STUDY = [
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('DU', 'Dual'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', default='users/default_user.webp', blank=True, null=True)
    place_of_study = models.CharField(max_length=255, blank=True)
    form_of_study = models.CharField(max_length=2, choices=FORM_OF_STUDY, blank=True)
    
    books_received = models.ManyToManyField(Book, through='BookReceipt', blank=True)

    def __str__(self) -> str:
        return f'{self.user.username}'


class BookReceipt(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='receipts')
    date_received = models.DateField(auto_now_add=True)
    date_due = models.DateField(default=datetime.now()+timedelta(weeks=1))

    class Meta:
        unique_together = ('profile', 'book')

    def __str__(self):
        return f'{self.book.title} received by {self.profile.user.username}'
    
    def save(self, *args, **kwargs):
        if self.profile.books_received.count() >= 3:
            raise ValidationError('A user can only receive up to 3 books.')
        super().save(*args, **kwargs)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.subject}'
