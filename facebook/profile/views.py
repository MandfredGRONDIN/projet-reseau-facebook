from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import ProfileForm
from post.models import Post
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from friendship.models import Friendship
from django.db.models import Q, Count
from post.forms import PostForm
from django.shortcuts import redirect

class ProfileView(TemplateView):
    template_name = 'profile.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = kwargs['pk']
        user = get_object_or_404(User, pk=pk)
        current_user = self.request.user

        context['profile'] = user.profile
        context['posts'] = Post.objects.filter(user=user)
        context['form'] = PostForm()

        # Vérifier l'amitié si ce n'est pas le profil de l'utilisateur actuel
        if current_user != user:
            friendship = Friendship.objects.filter(
                Q(user1=current_user, user2=user) | Q(user1=user, user2=current_user)
            ).first()
            context['friendship'] = friendship

        posts = Post.objects.filter(user=self.request.user).order_by('-created_at')

        reactions_count = []
        for post in posts:
            # Comptage des réactions par type et création d'une liste de dicts
            reaction_count = post.reaction_set.values('type').annotate(count=Count('type'))
            reactions_count.append({
                'post_id': post.id,
                'reactions': reaction_count
            })

        # Ajouter la liste des réactions dans le context
        context['reactions_count'] = reactions_count

        return context
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
        return redirect('profile', pk=request.user.pk) 
    
class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})
