from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.users.models import Profile


class AuthRecaptchaTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='johndoe',
            email='john@example.com',
            password='SecretPassword123!',
            first_name='John',
            last_name='Doe'
        )

    def test_register_success(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'StrongP@ss123!',
            'password2': 'StrongP@ss123!',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_duplicate_email(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'anotheruser',
            'email': 'john@example.com',  # already taken by self.user
            'password1': 'StrongP@ss123!',
            'password2': 'StrongP@ss123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='anotheruser').exists())

    def test_login_first_visit_no_recaptcha(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['show_recaptcha'])

    def test_login_first_failure_triggers_recaptcha(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'johndoe',
            'password': 'WrongPassword!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['show_recaptcha'])
        self.assertEqual(self.client.session['failed_login_attempts'], 1)

    def test_login_requires_recaptcha_after_failure(self):
        # 1st fail
        self.client.post(reverse('users:login'), {
            'username': 'johndoe',
            'password': 'WrongPassword!',
        })
        # 2nd attempt with correct password but without recaptcha
        response = self.client.post(reverse('users:login'), {
            'username': 'johndoe',
            'password': 'SecretPassword123!',
            'g-recaptcha-response': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['recaptcha_error'])
        # User should not be logged in
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_login_success_with_recaptcha_resets_counter(self):
        # 1st fail
        self.client.post(reverse('users:login'), {
            'username': 'johndoe',
            'password': 'WrongPassword!',
        })
        # 2nd attempt with valid credentials and recaptcha
        response = self.client.post(reverse('users:login'), {
            'username': 'johndoe',
            'password': 'SecretPassword123!',
            'g-recaptcha-response': 'test-valid-token',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertIsNone(self.client.session.get('failed_login_attempts'))

    def test_logout(self):
        self.client.login(username='johndoe', password='SecretPassword123!')
        response = self.client.get(reverse('users:logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_profile_one_to_one_auto_creation(self):
        # Signal orqali User yaratilganda Profile ham yaratilganini tekshiramiz
        self.assertIsNotNone(self.user.profile)
        self.assertEqual(self.user.profile.user, self.user)

    def test_profile_view_requires_login(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('users:login'), response.url)

    def test_profile_view_get_authenticated(self):
        self.client.login(username='johndoe', password='SecretPassword123!')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'johndoe')
        self.assertContains(response, 'Profilni tahrirlash')

    def test_profile_view_update_post(self):
        self.client.login(username='johndoe', password='SecretPassword123!')
        response = self.client.post(reverse('users:profile'), {
            'first_name': 'Johnny',
            'last_name': 'Doeman',
            'email': 'johnny@example.com',
            'phone_number': '+998901234567',
            'address': 'Toshkent sh., Chilonzor',
            'bio': 'Salom, men xaridorman!',
        }, follow=True)
        self.assertEqual(response.status_code, 200)

        # Bazada o'zgarishlarni tekshiramiz
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Johnny')
        self.assertEqual(self.user.email, 'johnny@example.com')
        self.assertEqual(self.user.profile.phone_number, '+998901234567')
        self.assertEqual(self.user.profile.address, 'Toshkent sh., Chilonzor')
        self.assertEqual(self.user.profile.bio, 'Salom, men xaridorman!')
