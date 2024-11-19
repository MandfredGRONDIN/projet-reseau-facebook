from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import ProfileForm
from post.models import Post
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from friendship.models import Friendship
from django.db.models import Q


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

        if current_user != user:  
            friendship = Friendship.objects.filter(
                Q(user1=current_user, user2=user) | Q(user1=user, user2=current_user)
            ).first()
            context['friendship'] = friendship

        return context
    
class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})
