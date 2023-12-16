from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm, CreateNewPost, DemandForm, UserProfileForm
from .models import Post, User, UserProfile
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models.signals import post_save
from django.dispatch import receiver

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
            print('Login bem-sucedido.')
            return redirect('home')
        else:
            error_message = 'Login inválido. Por favor, tente novamente.'
            print('Login inválido. Por favor, tente novamente.')
            messages.error(request, error_message, extra_tags='INVALID_LOGIN_ERROR')

    return render(request, 'login.html')

@login_required
def home(request, selected_username=None):
    current_user = request.user
    
    if current_user.is_authenticated:
        posts = Post.objects.all()  # Retrieve all instances of a post

        if selected_username:
            # If a user is selected, retrieve the UserProfile instance
            try:
                user_profile = UserProfile.objects.get(user__username=selected_username)
            except UserProfile.DoesNotExist:
                # Handle the case when the selected user does not exist
                user_profile = None
        else:
            # If no user is selected, use the current user's profile
            user_profile = current_user.userprofile

        return render(request, 'home.html', {'posts': posts, 'user_profile': user_profile})
    else:
        return redirect('login')

def post_create(request):
  if request.method == 'POST':
        form = DemandForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  
            post.save()
            return redirect('home')
        else:
            error_message = 'Every post must have an image. Try again!'
            messages.error(request, error_message, extra_tags='IMAGE_BLANK_ERROR')
  else:
        form = DemandForm()

  return render(request, 'createnewpost.html', {'form': form})
  
@login_required
def like_a_post(request):
    post = get_object_or_404(post, id=request.POST.get('post_id'))
    post.likes += 1
    post.who_liked.add(request.user)
    post.save()
    return HttpResponseRedirect(post.get_absolute_url())

@login_required
def logoutPage(request):
    logout(request)
    return redirect('login')

@receiver(post_save, sender=User)
def create_profile (sender, instance, created, **kwargs):
    if created:
        print('Profile created!')
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile (sender, instance, **kwargs):
    print('Profile saved!')
    instance.userprofile.save()

@login_required
def view_profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
        user_profile = get_object_or_404(UserProfile, user=user)
        is_own_profile = False
    else:
        user_profile = request.user.userprofile
        is_own_profile = True

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'user_profile': user_profile,
        'is_own_profile': is_own_profile,
        'form': form,
    }

    return render(request, 'profile.html', context)


