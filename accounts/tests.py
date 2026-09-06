from django.test import TestCase
from django.urls import reverse
from .models import CustomUser


class AuthFlowTests(TestCase):
    def test_signup_creates_user(self):
        response = self.client.post(reverse("accounts:signup"), {
            "email": "teststudent@example.com",
            "password1": "a-very-strong-test-pass-2026",
            "password2": "a-very-strong-test-pass-2026",
        })
        self.assertEqual(CustomUser.objects.filter(email="teststudent@example.com").count(), 1)

    def test_login_with_correct_credentials(self):
        CustomUser.objects.create_user(email="student@example.com", password="correct-pass-2026")
        response = self.client.post(reverse("accounts:login"), {
            "username": "student@example.com",
            "password": "correct-pass-2026",
        })
        self.assertEqual(response.status_code, 302)
    def test_login_with_wrong_password_fails(self):
        CustomUser.objects.create_user(email="student@example.com", password="correct-pass-2026")
        response = self.client.post(reverse("accounts:login"), {
            "username": "student@example.com",
            "password": "wrong-password",
        })
        self.assertEqual(response.status_code, 200)
    def test_anonymous_user_redirected_from_lessons(self):
        response = self.client.get("/lessons/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("next=/lessons/", response.url)