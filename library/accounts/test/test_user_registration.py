from django.test import TestCase
from django.contrib.auth import get_user_model
from ..forms import UserRegistrationForm

User = get_user_model()

class UserRegistrationFormTest(TestCase):
    
    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'asdfgh5002',
            'password2': 'asdfgh5002'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_duplicate_email(self):
        User.objects.create_user(username='testuser2', email='test@example.com', password='asdfgh5002')
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'test@example.com',  # Duplicate email
            'password1': 'asdfgh5002',
            'password2': 'asdfgh5002'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_short_username(self):
        form_data = {
            'username': 'tu',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
