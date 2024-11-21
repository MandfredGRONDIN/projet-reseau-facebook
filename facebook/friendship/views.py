from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, RedirectView
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Friendship
from django.views.generic import View
from share.models import Share
   
class UserSearchView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'search_results.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return User.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )
        return User.objects.none()

class SendFriendRequestView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user2 = get_object_or_404(User, pk=kwargs['pk'])

        # Vérifier si c'est une auto-demande
        if user2 == self.request.user:
            return reverse('profile', kwargs={'pk': user2.pk})

        # Vérifier les demandes existantes
        friendship, created = Friendship.objects.get_or_create(
            user1=self.request.user, user2=user2,
            defaults={'status': Friendship.PENDING}
        )

        if not created and friendship.status == Friendship.PENDING:
            # Une demande existe déjà
            return reverse('profile', kwargs={'pk': user2.pk})

        return reverse('profile', kwargs={'pk': user2.pk})

class RespondToFriendRequestView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        action = kwargs.get('action') 
        user2 = get_object_or_404(User, pk=kwargs['pk'])

        # Rechercher la demande d’amitié en attente
        friendship = get_object_or_404(
            Friendship,
            user1=user2,
            user2=self.request.user,
            status=Friendship.PENDING
        )

        if action == 'accept':
            friendship.status = Friendship.ACCEPTED
        elif action == 'reject':
            friendship.status = Friendship.REJECTED

        friendship.save()
        return reverse('home')
    
class RemoveFriendView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Récupérer l'utilisateur (ami) à supprimer
        user2 = get_object_or_404(User, pk=pk)

        # Trouver les relations d'amitié entre les deux utilisateurs
        friendships = Friendship.objects.filter(
            (Q(user1=request.user) & Q(user2=user2)) |
            (Q(user1=user2) & Q(user2=request.user))
        )

        # Si la relation d'amitié existe, la supprimer
        if friendships.exists():
            friendships.delete()
            
            shares_to_delete = Share.objects.filter(
                Q(user=request.user) & Q(post__user=user2)
            )
            shares_to_delete.delete()
        
        return redirect('home')