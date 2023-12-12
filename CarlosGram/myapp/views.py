from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm, CreateNewPost, DemandForm
from .models import post
from django.http import HttpResponse
# Create your views here.
def signup(request):    
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            print(f'User {user.username} created successfully!')  # Add this print statement
            login(request, user)
            messages.success(request, f'Conta criada para {user.username}!')
            form.save()
            
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Login bem-sucedido para {username}!')
            print('Login bem-sucedido.')
            return redirect('home')
        else:
            print('Login inválido. Por favor, tente novamente.')
            messages.error(request, 'Login inválido. Por favor, tente novamente.')

    return render(request, 'login.html')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def post_create(request):
  if request.method == 'POST':
        form = DemandForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  
            post.save()
            return redirect('home')
  else:
        form = DemandForm()

  return render(request, 'createnewpost.html', {'form': form})
  