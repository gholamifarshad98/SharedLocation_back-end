# api/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserLocationSerializer, SharedUserSerializer, AllowedUserSerializer
from .models import UserLocation, SharedUser, AllowedUser
from rest_framework.permissions import AllowAny, IsAuthenticated

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
                'user_id': user.id
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        locations = UserLocation.objects.filter(user=request.user).order_by('-last_updated')
        serializer = UserLocationSerializer(locations, many=True)
        print(f"User {request.user.username} locations: {serializer.data}")  # Debug
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        print('POST Request data:', data)  # Debug incoming data
        if not request.user.is_authenticated:
            print("User not authenticated")
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserLocationSerializer(data=data, context={'user': request.user})
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)  # Pass user explicitly to serializer
                print(f"Location saved for {request.user.username}: {serializer.data}")  # Debug
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(f"Save error: {str(e)}")  # Debug
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print('Serializer errors:', serializer.errors)  # Debug
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SharedUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shared_users = SharedUser.objects.filter(owner=request.user)
        serializer = SharedUserSerializer(shared_users, many=True)
        print(f"Shared users for {request.user.username}: {serializer.data}")  # Debug
        return Response(serializer.data)

    def delete(self, request, shared_user_id=None):
        try:
            shared_user = SharedUser.objects.get(id=shared_user_id, owner=request.user)
            shared_user.delete()
            print(f"Deleted shared user {shared_user_id} for {request.user.username}")  # Debug
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SharedUser.DoesNotExist:
            return Response({'error': 'Shared user not found'}, status=status.HTTP_404_NOT_FOUND)

class AllowedUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        allowed_users = AllowedUser.objects.filter(owner=request.user)
        serializer = AllowedUserSerializer(allowed_users, many=True)
        print(f"Allowed users for {request.user.username}: {serializer.data}")  # Debug
        return Response(serializer.data)

    def post(self, request):
        username = request.data.get('username')
        print(f"Allowing user {username} for {request.user.username}")  # Debug
        try:
            allowed_to_user = User.objects.get(username=username)
            if allowed_to_user == request.user:
                return Response({'error': 'Cannot allow yourself'}, status=status.HTTP_400_BAD_REQUEST)
            allowed_user, created = AllowedUser.objects.get_or_create(
                owner=request.user,
                allowed_to=allowed_to_user
            )
            serializer = AllowedUserSerializer(allowed_user)
            print(f"{'Created' if created else 'Updated'} allowed user: {serializer.data}")  # Debug
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, allowed_user_id=None):
        try:
            allowed_user = AllowedUser.objects.get(id=allowed_user_id, owner=request.user)
            allowed_user.delete()
            print(f"Deleted allowed user {allowed_user_id} for {request.user.username}")  # Debug
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AllowedUser.DoesNotExist:
            return Response({'error': 'Allowed user not found'}, status=status.HTTP_404_NOT_FOUND)

class UserLocationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        print(f"Fetching locations for user_id {user_id} by {request.user.username}")
        try:
            target_user = User.objects.get(id=user_id)
            # Check if requester is the target user, has SharedUser, or has AllowedUser permission
            if (request.user == target_user or 
                SharedUser.objects.filter(owner=target_user, shared_with=request.user).exists() or 
                AllowedUser.objects.filter(owner=target_user, allowed_to=request.user).exists()):
                locations = UserLocation.objects.filter(user=target_user).order_by('-last_updated')
                if not locations.exists():
                    print(f"No locations found for user {target_user.username}")
                    return Response([], status=status.HTTP_200_OK)  # Empty list if no locations
                serializer = UserLocationSerializer(locations, many=True)
                print(f"Locations for {target_user.username}: {serializer.data}")
                return Response(serializer.data)
            print(f"Permission denied for {request.user.username} to view {target_user.username}'s locations")
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            print(f"User {user_id} not found")
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)