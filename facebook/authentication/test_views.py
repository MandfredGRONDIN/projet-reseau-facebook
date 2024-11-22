from django.test import TestCase
from django.contrib.auth.models import User
from story.models import Story
from post.models import Post
from friendship.models import Friendship
from django.utils import timezone
from datetime import timedelta

class HomeViewTest(TestCase):
    def setUp(self):
        print("Configuration initiale des tests...")
        
        # Créer un utilisateur et un ami
        self.user = User.objects.create_user(username='testuser', password='password')
        self.friend = User.objects.create_user(username='frienduser', password='password')
        self.pending_friend = User.objects.create_user(username='pendingfriend', password='password')

        # Créer une relation d'amitié acceptée
        Friendship.objects.create(user1=self.user, user2=self.friend, status=Friendship.ACCEPTED)
        
        # Créer une demande d'amitié en attente
        Friendship.objects.create(user1=self.pending_friend, user2=self.user, status=Friendship.PENDING)

        # Créer des stories
        self.user_story = Story.objects.create(
            user=self.user,
            media_url="http://example.com/user_story.jpg",
            expiration_date=timezone.now() + timedelta(days=1)
        )
        self.friend_story = Story.objects.create(
            user=self.friend,
            media_url="http://example.com/friend_story.jpg",
            expiration_date=timezone.now() + timedelta(days=1)
        )
        self.expired_story = Story.objects.create(
            user=self.user,
            media_url="http://example.com/expired_story.jpg",
            expiration_date=timezone.now() - timedelta(days=1)
        )

        # Créer un post
        self.user_post = Post.objects.create(user=self.user, content="Hello, world!")
        print("Configuration initiale terminée.")

    def test_home_view_authenticated_user(self):
        print("Test : Vue home pour un utilisateur authentifié")
        self.client.login(username='testuser', password='password')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user_post.content)
        self.assertContains(response, self.user_story.media_url)
        self.assertNotContains(response, self.expired_story.media_url)  
        print("✔ Vue home pour un utilisateur authentifié : OK")

    def test_home_view_unauthenticated_user(self):
        print("Test : Redirection pour un utilisateur non authentifié")
        response = self.client.get('/')
        self.assertRedirects(response, '/login/?next=/')
        print("✔ Redirection pour un utilisateur non authentifié : OK")

    def test_post_submission(self):
        print("Test : Soumission de post")
        self.client.login(username='testuser', password='password')

        response = self.client.post('/', {'content': 'New Post'})
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Post.objects.filter(content='New Post').exists())
        print("✔ Soumission de post : OK")


    def test_friends_displayed_in_view(self):
        print("Test : Affichage des amis dans la vue")
        self.client.login(username='testuser', password='password')
        response = self.client.get('/')
        self.assertContains(response, self.friend.username)
        print("✔ Affichage des amis dans la vue : OK")

    def test_story_expiration(self):
        print("Test : Les stories expirées ne doivent pas apparaître")
        self.client.login(username='testuser', password='password')
        response = self.client.get('/')
        self.assertNotContains(response, self.expired_story.media_url)  
        print("✔ Les stories expirées ne sont pas affichées : OK")
