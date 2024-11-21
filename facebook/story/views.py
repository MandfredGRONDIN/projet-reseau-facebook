from django.views.generic import CreateView, DetailView, ListView
from django.utils import timezone
from .models import Story
from .forms import StoryForm
from django.urls import reverse_lazy
from django.db.models import Q
from friendship.models import Friendship

class CreateStoryView(CreateView):
    model = Story
    form_class = StoryForm
    template_name = 'create_story.html'
    success_url = reverse_lazy('home') 

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class StoryListView(ListView):
    model = Story
    template_name = 'story_list.html'
    context_object_name = 'stories'
    
    def get_queryset(self):
        # Récupérer les stories de l'utilisateur connecté
        user_stories = Story.objects.filter(
            user=self.request.user,
            expiration_date__gte=timezone.now()  # Stories non expirées de l'utilisateur
        )
        
        # Récupérer les amis de l'utilisateur connecté
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
        
        # Récupérer les stories des amis
        friend_stories = Story.objects.filter(
            user__in=friend_users,
            expiration_date__gte=timezone.now()  # Stories non expirées des amis
        )
        
        # Combine les stories de l'utilisateur et de ses amis
        stories = user_stories | friend_stories
        
        # Trier les stories combinées par date de création descendante
        return stories.order_by('-created_at')
    
class StoryDetailView(DetailView):
    model = Story
    template_name = 'view_story.html'  
    context_object_name = 'story' 

    def get_object(self, queryset=None):
        return super().get_object(queryset)