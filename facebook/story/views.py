from django.views.generic import CreateView, DetailView, ListView
from django.utils import timezone
from .models import Story
from .forms import StoryForm
from django.urls import reverse_lazy

class CreateStoryView(CreateView):
    model = Story
    form_class = StoryForm
    template_name = 'create_story.html'
    success_url = reverse_lazy('story_list') 

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class StoryListView(ListView):
    model = Story
    template_name = 'story_list.html'
    context_object_name = 'stories'
    
    def get_queryset(self):

        return Story.objects.filter(expiration_date__gte=timezone.now())

class StoryDetailView(DetailView):
    model = Story
    template_name = 'view_story.html'  
    context_object_name = 'story' 

    def get_object(self, queryset=None):
        return super().get_object(queryset)