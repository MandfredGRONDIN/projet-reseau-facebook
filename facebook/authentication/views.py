from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views import View
from .forms import UserRegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from profile.models import Profile
from .forms import EmailLoginForm
from django.shortcuts import render
from django.views.generic import TemplateView
from post.models import Post
from post.forms import PostForm
from friendship.models import Friendship
from django.db.models import Count,Q

# Home View
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = '/login/'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupérer les posts de l'utilisateur connecté
        user_posts = Post.objects.filter(user=self.request.user).order_by('-created_at')

        friends = Friendship.objects.filter(
            Q(user1=self.request.user, status=Friendship.ACCEPTED) |
            Q(user2=self.request.user, status=Friendship.ACCEPTED)
        )

        # Récupérer les utilisateurs amis
        friend_users = set()
        for friendship in friends:
            if friendship.user1 == self.request.user:
                friend_users.add(friendship.user2)
            else:
                friend_users.add(friendship.user1)

        # Récupérer les posts des amis
        friend_posts = Post.objects.filter(user__in=friend_users).order_by('-created_at')

        # Combiner les posts de l'utilisateur et des amis
        posts = user_posts | friend_posts

        # Ajouter les posts dans le context
        context['posts'] = posts.order_by('-created_at')
        context['form'] = PostForm()

        # Calcul des réactions pour chaque post
        reactions_count = []
        for post in posts:
            reaction_count = post.reaction_set.values('type').annotate(count=Count('type'))
            reactions_count.append({
                'post_id': post.id,
                'reactions': reaction_count
            })

        # Ajouter la liste des réactions dans le context
        context['reactions_count'] = reactions_count

        # Récupération des demandes d'amitié reçues
        context['friend_requests'] = Friendship.objects.filter(
            user2=self.request.user,  
            status=Friendship.PENDING
        )

        # Liste des utilisateurs amis pour le template
        context['friends'] = friend_users 

        return context
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
        return redirect('home') 
      

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