# core/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, Conversation, ChatMessage
from .forms import CustomUserCreationForm
from django.forms import BaseForm

# Creates test user
def create_test_user(username="testuser", password="Test1ng2001#", email="test@example.com", first_name="Test", last_name="User"):
    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
    # Ensure UserProfile exists, creating if necessary
    profile, created = UserProfile.objects.get_or_create(user=user)
    return user


#Tests authentication
class AuthViewsCoreTest(TestCase):
    # sets up navigation for tests
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')
        self.chat_url = reverse('chat')
        self.quiz_url = reverse('persona_quiz')
        self.strong_password = "Test1ng2001#"

    # testing the registration page loads
    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/register.html')
        self.assertIsInstance(response.context.get('form'), CustomUserCreationForm)

    # testing user registration works
    def test_register_view_post_success(self):
        User.objects.all().delete()
        UserProfile.objects.all().delete()
        user_count_before = User.objects.count()

        registration_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new@example.com',
            'password1': self.strong_password,
            'password2': self.strong_password,
            'phone_number': '',
        }
        response = self.client.post(self.register_url, registration_data, follow=False)

        # Checks redirect to persona quiz
        error_detail = "N/A"
        if response.status_code != 302 and hasattr(response, 'context'):
            form_in_context = response.context.get('form')
            if form_in_context and isinstance(form_in_context, BaseForm) and hasattr(form_in_context, 'errors'):
                 error_detail = form_in_context.errors
            else:
                 error_detail = f"Response context might be missing or form not in context. Status: {response.status_code}"

        self.assertEqual(response.status_code, 302,
                         f"Registration POST did not redirect as expected. Status: {response.status_code}. Form errors/details: {error_detail}")
        self.assertEqual(response.url, self.quiz_url)

        # Verify user and profile were created
        self.assertEqual(User.objects.count(), user_count_before + 1)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(UserProfile.objects.filter(user__username='newuser').exists())

        # Verify user is logged in (can access a protected page like quiz)
        login_success = self.client.login(username='newuser', password=self.strong_password)
        self.assertTrue(login_success, f"Could not log in with new user 'newuser' and password '{self.strong_password}'")
        response_quiz = self.client.get(self.quiz_url)
        self.assertEqual(response_quiz.status_code, 200, f"Could not access quiz page after registration and login. Status: {response_quiz.status_code}")

    # test login page is functional
    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')
    # tests login success
    def test_login_view_post_success(self):
        user = create_test_user(username='testuser_login', password=self.strong_password)
        response = self.client.post(self.login_url, {
            'username': 'testuser_login',
            'password': self.strong_password,
        })
        # Successful login redirects to /chat/, which itself redirects (target_status_code=302)
        self.assertRedirects(response, self.chat_url, status_code=302, target_status_code=302, fetch_redirect_response=False)
        # Check session
        self.assertTrue('_auth_user_id' in self.client.session)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
    # tests login fail
    def test_login_view_post_fail(self):
        user = create_test_user(username='testuser_fail', password=self.strong_password)
        response = self.client.post(self.login_url, {
            'username': 'testuser_fail',
            'password': 'wrongpassword123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')
        self.assertFalse('_auth_user_id' in self.client.session)
        form_in_context = response.context.get('form')
        self.assertTrue(form_in_context and isinstance(form_in_context, BaseForm) and form_in_context.errors)
    # test logout redirection to homepage
    def test_logout_view(self):
        user = create_test_user(username='testuser_logout', password=self.strong_password)
        self.client.login(username='testuser_logout', password=self.strong_password)
        self.assertTrue('_auth_user_id' in self.client.session)
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.home_url, status_code=302, target_status_code=200)
        self.assertFalse('_auth_user_id' in self.client.session)


class ChatViewCoreTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.strong_password = "Test1ng2001#"
        self.user = create_test_user(username='chat_user', password=self.strong_password)
        self.client.login(username='chat_user', password=self.strong_password)
        self.chat_redirect_url = reverse('chat')
        self.chat_new_url = reverse('chat_new')

    def test_chat_redirect_view_authenticated(self):
        response = self.client.get(self.chat_redirect_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/chat/'))
        self.assertNotEqual(response.url, self.chat_redirect_url)
    # Tests creating new chat redirects to new url
    def test_new_chat_view(self):
        conversation_count_before = Conversation.objects.filter(user=self.user).count()
        response = self.client.get(self.chat_new_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Conversation.objects.filter(user=self.user).count(), conversation_count_before + 1)
        new_convo = Conversation.objects.filter(user=self.user).latest('created_at')
        expected_url = reverse('chat_with_id', args=[new_convo.id])
        self.assertEqual(response.url, expected_url)
    # Testing chat history works
    def test_chat_view_get_loads(self):
        convo = Conversation.objects.create(user=self.user, title="Test Convo")
        ChatMessage.objects.create(user=self.user, conversation=convo, message="Hi, hello I am testing", role="user")
        chat_url = reverse('chat_with_id', args=[convo.id])
        response = self.client.get(chat_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/chat.html')
        self.assertContains(response, "Hi, hello I am testing")
        self.assertEqual(response.context.get('conversation'), convo)
    # Testing conversation deletion and redirection
    def test_delete_conversation_view(self):
        convo_to_delete = Conversation.objects.create(user=self.user, title="Delete Me")
        convo_id = convo_to_delete.id
        delete_url = reverse('delete_conversation', args=[convo_id])
        conversation_count_before = Conversation.objects.filter(user=self.user).count()
        response = self.client.post(delete_url)
        if Conversation.objects.filter(user=self.user).exists():
            latest_remaining = Conversation.objects.filter(user=self.user).latest('created_at')
            expected_redirect_url = reverse('chat_with_id', args=[latest_remaining.id])
        else:
            expected_redirect_url = reverse('chat_new')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_redirect_url)
        self.assertEqual(Conversation.objects.filter(user=self.user).count(), conversation_count_before - 1)
        self.assertFalse(Conversation.objects.filter(id=convo_id).exists())


# testing the persona can be viewed
class ProfileViewCoreTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.strong_password = "Test1ng2001#"
        self.user = create_test_user(username='profile_user', password=self.strong_password, first_name="ProfileTest")
        self.client.login(username='profile_user', password=self.strong_password)
        self.profile_url = reverse('profile')

    def test_profile_view_get_loads(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/profile.html')
        self.assertContains(response, "ProfileTest")

# tests persona quiz
class PersonaQuizCoreTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.strong_password = "Test1ng2001#"
        self.user = create_test_user(username='quiz_user', password=self.strong_password)
        self.profile = UserProfile.objects.get(user=self.user)
        self.client.login(username='quiz_user', password=self.strong_password)
        self.quiz_url = reverse('persona_quiz')
        self.result_url = reverse('persona_result')

    def test_quiz_view_get_no_persona(self):
        self.profile.persona = ""
        self.profile.save()
        response = self.client.get(self.quiz_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/persona_quiz.html')

    def test_quiz_view_post_success(self):
        self.profile.persona = ""
        self.profile.save()
        quiz_data = {
            'q1': 'tech', 'q2': 'tech', 'q3': 'tech', 'q4': 'tech', 'q5': 'tech'
        }
        response = self.client.post(self.quiz_url, quiz_data)
        self.assertRedirects(response, self.result_url, status_code=302, target_status_code=200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.persona, 'tech')

    def test_result_view_get_persona_exists(self):
        self.profile.persona = "luxury"
        self.profile.save()
        response = self.client.get(self.result_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/persona_result.html')
        self.assertContains(response, "Luxury Seeker")

    def test_result_view_redirects_if_no_persona(self):
        self.profile.persona = ""
        self.profile.save()
        response = self.client.get(self.result_url)
        self.assertRedirects(response, self.quiz_url, status_code=302, target_status_code=200)

