from django.views.generic.edit import CreateView
from .models import Post
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create_post.html'
    success_url = '/' 
    
    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)
