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

# Home View
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = '/login/'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(user=self.request.user).order_by('-created_at')
        context['form'] = PostForm()  
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