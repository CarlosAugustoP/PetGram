from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm

# Create your views here.
def home(request):    
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
    return render(request, 'home.html', {'form': form})

def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Login bem-sucedido para {username}!')
            print('Login bem-sucedido.')
             
        else:
            print('Login inválido. Por favor, tente novamente.')
            messages.error(request, 'Login inválido. Por favor, tente novamente.')

    return render(request, 'login.html')
