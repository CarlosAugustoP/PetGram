from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import User,Post, UserProfile, Comment
class SignupForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2', 'phone', 'address']

class CreateNewPost(forms.Form):
  class Meta:
    model = Post
    fields = ['image', 'caption']

class DemandForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description','image']
        labels = {

          'description': 'Descrição',
          
        }

class UserProfileForm(forms.ModelForm):
   class Meta:
      model = UserProfile
      fields = ['profile_image', 'bio']
      labels = {
          'profile_image': 'Foto de perfil',
      }

class CommentForm(forms.ModelForm):
   class Meta:
      model = Comment
      fields = ['comment']
      labels = {
          'comment': 'Comentário',
      }

    