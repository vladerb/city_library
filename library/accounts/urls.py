from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('reg/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(next_page='accounts:user-login'), name='user-logout'),
    
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/edit/', views.UserProfileEditView.as_view(), name='user-profile-edit'),
    path('profile/password/', views.CustomPasswordChangeView.as_view(), name='user-password-edit'),
    
]