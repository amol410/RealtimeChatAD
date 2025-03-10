from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q, OuterRef, Subquery
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
from .models import ChatMessage, User
from .serializers import MessageSerializer, UserSerializer, LoginSerializer
from .backends import EmailBackend

logger = logging.getLogger(__name__)  # Logger for debugging

# ✅ Registration View with Explicit Authentication Backend
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # ✅ Explicitly set authentication backend
        user.backend = 'Chat.backends.EmailBackend'
        login(request, user, backend='Chat.backends.EmailBackend')

        return Response({
            'user': serializer.data,
            'message': 'Registration successful'
        }, status=status.HTTP_201_CREATED)


# ✅ Login View with Proper User Authentication
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

        # Check if the user exists
        user_exists = User.objects.filter(email=email).exists()
        if not user_exists:
            return Response({'error': 'No user found with this email'}, status=status.HTTP_401_UNAUTHORIZED)

        # Authenticate user using the custom backend
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # ✅ Explicitly set authentication backend before login
            user.backend = 'Chat.backends.EmailBackend'
            login(request, user, backend='Chat.backends.EmailBackend')

            return Response({
                'user': UserSerializer(user).data,
                'message': 'Login successful'
            })
        else:
            logger.debug("Authentication failed")  # Log failed authentication
            return Response({'error': 'Invalid credentials. Please check your email and password.'},
                            status=status.HTTP_401_UNAUTHORIZED)


# ✅ Logout View
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


# ✅ Inbox View to Get Last Messages
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


# ✅ Get Messages Between Two Users
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


# ✅ Send a Message
class SendMessage(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


# ✅ Chat History Between Two Users
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
