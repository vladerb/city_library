from django.test import TestCase
from django.urls import reverse
from ..models import Book, Category, Author

class BookDetailViewTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title="Test Category")
        self.author = Author.objects.create(name='Test author')
        self.book = Book.objects.create(title="Test Book", author=self.author, category=self.category)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/archive/books/{self.book.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('archive:book-detail', args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('archive:book-detail', args=[self.book.pk]))
        self.assertTemplateUsed(response, 'archive/book/book_detail.html')