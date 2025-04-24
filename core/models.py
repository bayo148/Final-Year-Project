from django.db import models
from django.contrib.auth.models import User

# extends Django's built-in User with more fields
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)

    PERSONA_CHOICES = [
        ("budget", "Budget Buyer"),
        ("luxury", "Luxury Seeker"),
        ("eco", "Eco‑Conscious"),
        ("tech", "Tech Enthusiast"),
        ("balanced", "Balanced Shopper"),
    ]
    persona = models.CharField(max_length=20, choices=PERSONA_CHOICES, blank=True)

    # translates the short code for personas to long form
    @property
    def persona_label(self):
        return dict(self.PERSONA_CHOICES).get(self.persona, "Unset")

    # Returns short description based on each persona
    @property
    def persona_description(self):
        desc = {
            "budget": "You love a great deal and value affordability.",
            "luxury": "Premium quality and prestige matter most to you.",
            "eco": "You prioritise sustainable and ethical products.",
            "tech": "Cutting‑edge specs and innovation excite you.",
            "balanced": "You shop with a mix of practicality, value, and quality.",
        }
        return desc.get(self.persona, "—")

    def __str__(self):
        return self.user.username

# represents individual user entire chat session
class Conversation(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
    title       = models.CharField(max_length=100, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    # snapshot of user persona
    persona = models.CharField(
        max_length=20,
        choices=UserProfile.PERSONA_CHOICES,
        blank=True,
        help_text="Snapshot of the user’s persona when the chat started",
    )

    def __str__(self):
        return self.title or f"Conversation {self.pk} – {self.created_at:%Y‑%m‑%d %H:%M}"

# each message sent in a chat session
class ChatMessage(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages", null=True, blank=True)
    message      = models.TextField()
    role         = models.CharField(max_length=20, default="user")
    timestamp    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} – {self.role}: {self.message[:30]}"