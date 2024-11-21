from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from post.models import Post
from .models import Share
from friendship.models import Friendship
from django.db.models import Q, Count
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from post.forms import PostForm

class SharePostView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        if Share.objects.filter(user=request.user, post=post).exists():
            messages.warning(request, "Vous avez déjà partagé ce post.")
        else:
            Share.objects.create(user=request.user, post=post)
            messages.success(request, "Vous avez partagé ce post.")
        
        return redirect('home')

class SharedPostsView(LoginRequiredMixin, ListView):
    template_name = 'shared_home.html'
    context_object_name = 'shared_posts'

    def get_queryset(self):
        # Récupérer les partages de l'utilisateur et de ses amis
        friends = Friendship.objects.filter(
            Q(user1=self.request.user, status=Friendship.ACCEPTED) |
            Q(user2=self.request.user, status=Friendship.ACCEPTED)
        )
        friend_users = {f.user2 if f.user1 == self.request.user else f.user1 for f in friends}

        # Récupérer les partages triés par date de partage descendante
        shares = Share.objects.filter(
            Q(user=self.request.user) | Q(user__in=friend_users)
        ).select_related('post', 'user').order_by('-created_at') 

        return shares 

    def get_context_data(self, **kwargs):
        # Obtenir le contexte de la classe parente
        context = super().get_context_data(**kwargs)

        # Ajouter la liste d'amis au contexte
        friendships = Friendship.objects.filter(
            Q(user1=self.request.user, status=Friendship.ACCEPTED) |
            Q(user2=self.request.user, status=Friendship.ACCEPTED)
        )
        friends = {f.user2 if f.user1 == self.request.user else f.user1 for f in friendships}
        context['friends'] = friends

        # Ajouter les demandes d'amitié reçues dans le contexte
        friend_requests = Friendship.objects.filter(
            user2=self.request.user,
            status=Friendship.PENDING
        )
        context['friend_requests'] = friend_requests
        
        context['form'] = PostForm()

        reactions_count = []
        for share in context['shared_posts']:
            reaction_count = share.post.reaction_set.values('type').annotate(count=Count('type'))
            reactions_count.append({
                'post_id': share.post.id,
                'reactions': reaction_count
            })
        context['reactions_count'] = reactions_count

        return context
