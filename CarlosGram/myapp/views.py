from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm, CreateNewPost, DemandForm, UserProfileForm, CommentForm
from .models import Post, User, UserProfile, Likes, Comment
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

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

def post_details (request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'post_details.html', {'post': post})

def post_create(request):
  if request.method == 'POST':
        form = DemandForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  
            post.user_profile = request.user.userprofile
            post.save()
            return redirect('home')
        else:
            error_message = 'Every post must have an image. Try again!'
            messages.error(request, error_message, extra_tags='IMAGE_BLANK_ERROR')
  else:
        form = DemandForm()

  return render(request, 'createnewpost.html', {'form': form})
  
@login_required
def like(request, post_id):
    user = request.user 
    post = Post.objects.get(id=post_id)
    current_likes = post.likes 
    liked = Likes.objects.filter(user = user, post =post).count() #check if user (currently logged in) has liked current post
    if not liked:# if a post is not liked, create an instance of a like for the current post
        liked = Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1 #increment like by 1
    else:
        Likes.objects.filter(user=user, post=post).delete() #delete instance of like if user clicks like again
        current_likes = current_likes - 1
    
    post.likes = current_likes #update current likes in post model 
    post.save() 
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) #redirect to the same page after liking post

@login_required
def home(request, selected_username=None):
    followers = request.user.followers.all()
    current_user = request.user
    users = User.objects.all()
    if current_user.is_authenticated:
        posts = Post.objects.all().order_by('-id') 
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

        # Get the liked posts for the current user
        liked_posts = Likes.objects.filter(user=current_user).values_list('post', flat=True)

        return render(request, 'home.html', {'posts': posts, 'user_profile': user_profile, 'liked_posts': liked_posts, 'users': users, 'followers': followers, 'current_user': current_user})
    else:
        return redirect('login')

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
    instance.userprofile.save()

@login_required
def view_profile(request, username=None):   
    current_user = request.user
    if username: #checkl if username exists 
        user = get_object_or_404(User, username=username) #if it does, get the user object
        if current_user in user.followers.all():
            is_following = True
        else:
            is_following = False
        posts = Post.objects.filter(user=user)
        user_profile = get_object_or_404(UserProfile, user=user) #get the user profile object
        if user == current_user:
            is_own_profile = True
        else:
            is_own_profile = False
    else:
        user = current_user
        posts = Post.objects.filter(user=user)
        user_profile = current_user.userprofile
        is_own_profile = True

    if request.method == 'POST':
        posts = Post.objects.filter(user=current_user)
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'user_profile': user_profile,
        'is_own_profile': is_own_profile,
        'form': form,
        'posts': posts,
        'username': user.username,
        'is_following': is_following
    }

    return render(request, 'profile.html', context)

@login_required
def comment (request, post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post)
    form = CommentForm(request.POST)
    current_user = request.user
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.user_profile = request.user.userprofile
            comment.post = post
            comment.save()
            post.comment += 1
            post.save()
            print(post.comment)
            print('Valid comment')
            
        else:
            error_message = 'Every comment must have a text. Try again!'
            messages.error(request, error_message, extra_tags='TEXT_BLANK_ERROR')
            print('Invalid comment')
    else:
        form = CommentForm()
    liked_posts = Likes.objects.filter(user=current_user).values_list('post', flat=True)
    return render(request, 'post_details.html', {'form': form , 'comments': comments, 'post': post, 'liked_posts': liked_posts})
        
@login_required
def follow(request, username):
    user = request.user #retrieve the current user
    following_user = User.objects.get(username=username) 
    #get the user that will be followed/unfollowed
    if user in following_user.followers.all(): 
        is_following = True
        print(is_following)
        print('Unfollowing user')
        following_user.followers.remove(user)
        user.following.remove(following_user)
        user.amount_of_following -= 1
        following_user.amount_of_followers -= 1
        following_user.save()
        user.save()
    else:
        print('Following user')
        is_following = False
        print(is_following)
        following_user.followers.add(user)
        user.following.add(following_user)
        user.amount_of_following += 1
        following_user.amount_of_followers += 1
        following_user.save()
        user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'is_following': is_following})