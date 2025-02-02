from django.shortcuts import render

# Create your views here.
# ------------ views.py ------------
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, OuterRef, Subquery
from .models import ChatMessage, User
from .serializers import MessageSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer, LoginSerializer
from rest_framework.permissions import AllowAny

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Log the user in after registration
        login(request, user)
        
        return Response({
            'user': serializer.data,
            'message': 'Registration successful'
        }, status=status.HTTP_201_CREATED)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__)

from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from .backends import EmailBackend  # Import the custom backend

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'error': 'Validation failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # Debug print
        logger.debug(f"Attempting login with email: {email}")
        
        # Try to get the user first
        try:
            user_exists = User.objects.filter(email=email).exists()
            if not user_exists:
                return Response({
                    'error': 'No user found with this email'
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error(f"Error checking user: {str(e)}")
        
        # Authenticate using the custom backend
        user = authenticate(request, email=email, password=password, backend='Chat.backends.EmailBackend')
        
        if user is not None:
            login(request, user)
            return Response({
                'user': UserSerializer(user).data,
                'message': 'Login successful'
            })
        else:
            # Check if password is being passed correctly
            logger.debug("Authentication failed")
            return Response({
                'error': 'Invalid credentials. Please check your email and password.'
            }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({
            'message': 'Logged out successfully'
        }, status=status.HTTP_200_OK)

class MyInbox(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatMessage.objects.filter(
            id__in=Subquery(
                User.objects.filter(
                    Q(sent_messages__receiver=user) |
                    Q(received_messages__sender=user)
                ).distinct().annotate(
                    last_msg=Subquery(
                        ChatMessage.objects.filter(
                            Q(sender=OuterRef('id'), receiver=user) |
                            Q(receiver=OuterRef('id'), sender=user)
                        ).order_by('-id')[:1].values_list('id')
                    )
                ).values_list('last_msg', flat=True)
            )
        ).order_by("-id")

class GetMessages(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        receiver_id = self.kwargs['receiver_id']
        return ChatMessage.objects.filter(
            (Q(sender=sender_id) & Q(receiver=receiver_id)) |
            (Q(sender=receiver_id) & Q(receiver=sender_id))
        ).order_by('date')

class SendMessage(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class ChatHistory(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        other_user_id = self.kwargs['user_id']
        return ChatMessage.objects.filter(
            (Q(sender=user) & Q(receiver=other_user_id)) |
            (Q(sender=other_user_id) & Q(receiver=user))
        ).order_by('date')