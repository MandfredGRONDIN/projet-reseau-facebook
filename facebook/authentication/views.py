from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views import View
from .forms import UserRegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from profile.models import Profile
from .forms import EmailLoginForm

# Home View
class HomeView(LoginRequiredMixin, View):
    login_url = '/login/' 

    def get(self, request):
        return render(request, 'home.html')
    
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

def login_view(request):
    if request.method == 'POST':
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
    else:
        form = EmailLoginForm()
    
    return render(request, 'login.html', {'form': form})