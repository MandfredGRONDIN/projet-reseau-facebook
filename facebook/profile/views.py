from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import ProfileForm
from post.models import Post

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['profile'] = user.profile
        context['posts'] = Post.objects.filter(user=user)  
        return context

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user.profile  

    def get_success_url(self):
        return reverse_lazy('profile')  
