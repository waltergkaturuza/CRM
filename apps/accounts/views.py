from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.db.models import Q
from .models import User, UserProfile, Team, Permission, RolePermission
from .serializers import (
    UserSerializer, UserProfileSerializer, TeamSerializer,
    PermissionSerializer, RolePermissionSerializer,
    LoginSerializer, RegisterSerializer, ChangePasswordSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model"""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['role', 'department', 'is_active']
    search_fields = ['first_name', 'last_name', 'email', 'username']
    ordering_fields = ['created_at', 'last_name', 'email']
    ordering = ['last_name']
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        user = self.request.user
        if user.role == 'admin':
            return User.objects.all()
        elif user.role == 'manager':
            return User.objects.filter(Q(manager=user) | Q(id=user.id))
        else:
            return User.objects.filter(id=user.id)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """Register a new user"""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """Login user"""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        """Update current user profile"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change user password"""
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for UserProfile model"""
    
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        user = self.request.user
        if user.role == 'admin':
            return UserProfile.objects.all()
        else:
            return UserProfile.objects.filter(user=user)
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get current user's profile"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'])
    def update_my_profile(self, request):
        """Update current user's profile"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for Team model"""
    
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['leader']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        user = self.request.user
        if user.role in ['admin', 'manager']:
            return Team.objects.all()
        else:
            return Team.objects.filter(members=user)
    
    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """Add member to team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                team.members.add(user)
                return Response({'message': 'Member added successfully'})
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        """Remove member from team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                team.members.remove(user)
                return Response({'message': 'Member removed successfully'})
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Permission model (read-only)"""
    
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['module']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'module']
    ordering = ['module', 'name']


class RolePermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for RolePermission model (read-only)"""
    
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['role']
    ordering_fields = ['role']
    ordering = ['role']
