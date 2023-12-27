"""
URL configuration for CarlosGram project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loginPage, name='index'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('create/', views.post_create, name='create'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/<str:username>/', views.view_profile, name='view_other_profile'),
    path('post/<str:post_id>/', views.post_details, name='post_details'),
    path('post/<str:post_id>/', views.like, name='like_post'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)