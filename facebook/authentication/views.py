from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views import View
from .forms import UserRegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from profile.models import Profile
from .forms import EmailLoginForm
from django.views.generic import TemplateView
from post.models import Post
from post.forms import PostForm
from friendship.models import Friendship
from django.db.models import Count,Q
from story.models import Story
from django.utils import timezone

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = '/login/'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Récupérer les amis de l'utilisateur
        friend_users = self.get_friend_users(self.request.user)

        # Récupérer les posts de l'utilisateur et de ses amis
        posts = self.get_user_and_friend_posts(self.request.user, friend_users)

        # Récupérer les stories de l'utilisateur et de ses amis
        stories = self.get_user_and_friend_stories(self.request.user, friend_users)

        # Calcul des réactions pour chaque post
        reactions_count = self.get_reactions_count(posts)

        # Ajouter au contexte
        context.update({
            'posts': posts.order_by('-created_at'),
            'stories': stories.order_by('-created_at'),
            'reactions_count': reactions_count,
            'form': PostForm(),
            'friend_requests': self.get_friend_requests(),
            'friends': friend_users
        })
        
        return context

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
        return redirect('home')

    def get_friend_users(self, user):
        """
        Récupère les utilisateurs amis de l'utilisateur donné.
        """
        friendships = Friendship.objects.filter(
            Q(user1=user, status=Friendship.ACCEPTED) |
            Q(user2=user, status=Friendship.ACCEPTED)
        )

        friend_users = set()
        for friendship in friendships:
            if friendship.user1 == user:
                friend_users.add(friendship.user2)
            else:
                friend_users.add(friendship.user1)
        
        return friend_users

    def get_user_and_friend_posts(self, user, friend_users):
        """
        Récupère les posts de l'utilisateur et de ses amis.
        """
        user_posts = Post.objects.filter(user=user).order_by('-created_at')
        friend_posts = Post.objects.filter(user__in=friend_users).order_by('-created_at')
        
        # Combiner les posts de l'utilisateur et de ses amis
        posts = user_posts | friend_posts
        return posts

    def get_user_and_friend_stories(self, user, friend_users):
        """
        Récupère les stories de l'utilisateur et de ses amis.
        """
        user_stories = Story.objects.filter(
            user=user,
            expiration_date__gte=timezone.now()
        )
        
        friend_stories = Story.objects.filter(
            user__in=friend_users,
            expiration_date__gte=timezone.now()
        ).order_by('-created_at')
        
        # Combiner les stories de l'utilisateur et de ses amis
        stories = user_stories | friend_stories
        return stories

    def get_reactions_count(self, posts):
        """
        Récupère le nombre de réactions pour chaque post.
        """
        reactions_count = []
        for post in posts:
            reaction_count = post.reaction_set.values('type').annotate(count=Count('type'))
            reactions_count.append({
                'post_id': post.id,
                'reactions': reaction_count
            })
        return reactions_count

    def get_friend_requests(self):
        """
        Récupère les demandes d'amitié en attente pour l'utilisateur connecté.
        """
        return Friendship.objects.filter(
            user2=self.request.user,
            status=Friendship.PENDING
        )

# Register View
class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  
            user.save()
            Profile.objects.create(user=user)
            login(request, user)  
            return redirect('home')  
        return render(request, 'register.html', {'form': form})

# Login View
class LoginView(View):
    def get(self, request):
        form = EmailLoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Email ou mot de passe invalide.')
        return render(request, 'login.html', {'form': form})
