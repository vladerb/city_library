from django.test import TestCase
from django.urls import reverse
from ..models import Book
from model_bakery import baker

class BookListViewTest(TestCase):
    
    def setUp(self) -> None:
        self.book1 = baker.make(Book, make_m2m=True)
        self.book2 = baker.make(Book, make_m2m=True)
        self.book3 = baker.make(Book, make_m2m=True)
        self.book4 = baker.make(Book, make_m2m=True)
        self.book5 = baker.make(Book, make_m2m=True)
        self.book6 = baker.make(Book, make_m2m=True)
        self.book7 = baker.make(Book, make_m2m=True)
        self.book8 = baker.make(Book, make_m2m=True)
        self.book9 = baker.make(Book, make_m2m=True)
        self.book10 = baker.make(Book, make_m2m=True)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 301)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('archive:books-list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('archive:books-list'))
        self.assertTemplateUsed(response, 'archive/book/book_list.html')

    def test_pagination_is_nine(self):
        response = self.client.get(reverse('archive:books-list'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['books']), 9)

    def test_lists_all_books(self):
        response = self.client.get(reverse('archive:books-list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['books']), 1)