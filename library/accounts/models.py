from django.contrib.auth import get_user_model
from django.db import models

from ..archive.models import Book

User = get_user_model()

class Profile(models.Model):
    FORM_OF_STUDY = [
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('DU', 'Dual'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', default='users/default_autor.webp', blank=True, null=True)
    place_of_study = models.CharField(max_length=255, blank=True)
    form_of_study = models.CharField(max_length=2, choices=FORM_OF_STUDY)
    
    books_received = models.ManyToManyField(Book, through='BookReceipt', blank=True)

    def __str__(self) -> str:
        return f'Profile of {self.user.username}'


class BookReceipt(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_received = models.DateField()
    date_due = models.DateField()

    class Meta:
        unique_together = ('profile', 'book')

    def __str__(self):
        return f'{self.book.title} received by {self.profile.user.username}'
