from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, FollowUserView, UserProfileView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('follow/<str:username>/', FollowUserView.as_view(), name='follow-user'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user-profile'),
]