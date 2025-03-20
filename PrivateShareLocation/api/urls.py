# api/urls.py
from django.urls import path
from .views import (
    RegisterView, LoginView, UserLocationView, 
    SharedUsersView, AllowedUsersView, UserLocationDetailView, AllowedByUsersView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('locations/', UserLocationView.as_view(), name='user-locations'),
    path('locations/<int:user_id>/', UserLocationDetailView.as_view(), name='user-location-detail'),
    path('shared-users/', SharedUsersView.as_view(), name='shared-users'),
    path('shared-users/<int:shared_user_id>/', SharedUsersView.as_view(), name='shared-user-delete'),
    path('allowed-users/', AllowedUsersView.as_view(), name='allowed-users'),
    path('allowed-users/<int:allowed_user_id>/', AllowedUsersView.as_view(), name='allowed-user-delete'),
    path('allowed-by-users/', AllowedByUsersView.as_view(), name='allowed-by-users'),
]