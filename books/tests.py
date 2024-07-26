# books/tests.py

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book

class BookModelTestCase(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            published_date="2023-01-01",
            isbn="1234567890123",
            pages=100,
            language="ENG"
        )

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, "Test Author")
        self.assertEqual(self.book.isbn, "1234567890123")
    
    def test_str_method(self):
        self.assertEqual(str(self.book), "Test Book")


class BookAPITestCase(APITestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            published_date="2023-01-01",
            isbn="1234567890123",
            pages=100,
            language="ENG"
        )
        self.list_create_url = reverse('book-list-create')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book.id})
    
    def test_list_books(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self):
        data = {
            "title": "New Book",
            "author": "New Author",
            "published_date": "2023-01-02",
            "isbn": "1234567890124",
            "pages": 200,
            "language": "FR"
        }
        response = self.client.post(self.list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_retrieve_book(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_book(self):
        data = {
            "title": "Updated Book",
            "author": "Updated Author",
            "published_date": "2023-01-03",
            "isbn": "1234567890123",
            "pages": 150,
            "language": "DE"
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())
