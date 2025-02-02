# ------------ models.py ------------
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    
    # Override the default username authentication to use email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    # Modified ManyToManyField definitions with unique related_names
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='chat_user_set',
        related_query_name='chat_user'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='chat_user_set',
        related_query_name='chat_user'
    )
    
    def profile(self):
        """
        Returns the user's profile if it exists, None otherwise.
        Uses property decorator to allow access as an attribute.
        """
        try:
            return self._profile
        except AttributeError:
            return None
    
    profile = property(profile)
    
    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=1000)
    bio = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="user_images", default="default.jpg")
    verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = self.user.username
        super().save(*args, **kwargs)

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="received_messages")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"{self.sender} to {self.receiver}"

    @property
    def sender_profile(self):
        return self.sender.profile
    
    @property
    def receiver_profile(self):
        return self.receiver.profile

# Signals for automatic profile creation
from django.db.models.signals import post_save
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
