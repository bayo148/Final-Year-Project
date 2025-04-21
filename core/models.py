from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Conversation(models.Model):
    """A single chat session owned by exactly one user."""
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
    title       = models.CharField(max_length=100, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or f"Conversation {self.pk} – {self.created_at:%Y‑%m‑%d %H:%M}"


class ChatMessage(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages", null=True, blank=True)
    message      = models.TextField()
    role         = models.CharField(max_length=20, default="user")  # 'user' | 'bot'
    timestamp    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} – {self.role}: {self.message[:30]}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username