# api/urls.py
from django.urls import path
from .views import (
    RegisterView, LoginView, UserLocationView, 
    SharedUsersView, AllowedUsersView, UserLocationDetailView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('locations/', UserLocationView.as_view(), name='user_locations'),
    path('shared-users/', SharedUsersView.as_view(), name='shared_users'),
    path('shared-users/<int:shared_user_id>/', SharedUsersView.as_view(), name='shared_user_delete'),
    path('allowed-users/', AllowedUsersView.as_view(), name='allowed_users'),
    path('allowed-users/<int:allowed_user_id>/', AllowedUsersView.as_view(), name='allowed_user_delete'),
    path('locations/<int:user_id>/', UserLocationDetailView.as_view(), name='user_location_detail'),
]
