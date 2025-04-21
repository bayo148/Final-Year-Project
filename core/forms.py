from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from .models import UserProfile


class ProfileUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "e.g. +44 1234 567890"})
    )
    address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Your address"})
    )

    class Meta:
        model = UserProfile
        fields = ["phone_number", "address"]

    def clean_phone_number(self):
        value = self.cleaned_data["phone_number"]
        if value and not re.fullmatch(r"\+?\d[\d\-\s]{7,}$", value):
            raise forms.ValidationError("Enter a valid phone number.")
        return value


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address']

class PersonaQuizForm(forms.Form):
    Q1_CHOICES = [
        ("budget",  "Finding the lowest price is crucial"),
        ("luxury",  "Brand reputation and quality matter most"),
        ("eco",     "Products must be eco-friendly and sustainable"),
        ("tech",    "I always look for the latest technology"),
        ("balanced",  "Convenience and ease matter more than specifics"),
    ]

    Q2_CHOICES = [
        ("budget",  "Always look for discounts or vouchers"),
        ("luxury",  "Only shop from premium or designer brands"),
        ("eco",     "Prefer products with sustainable certifications"),
        ("tech",    "Research extensively for cutting-edge specs"),
        ("balanced",  "Usually buy the most convenient option"),
    ]

    Q3_CHOICES = [
        ("budget",  "Less than £50"),
        ("balanced",  "£50 to £200"),
        ("tech",    "Willing to spend more if the product has advanced features"),
        ("eco",     "Flexible, as long as it’s eco-conscious"),
        ("luxury",  "Price is secondary; quality and luxury come first"),
    ]

    Q4_CHOICES = [
        ("budget",  "Primarily price comparison sites"),
        ("luxury",  "Luxury lifestyle magazines and blogs"),
        ("eco",     "Sustainability and ethical living resources"),
        ("tech",    "Tech reviews, blogs, and specification sites"),
        ("balanced",  "General social media and friend recommendations"),
    ]

    Q5_CHOICES = [
        ("budget",  "I'd rather buy multiple affordable items"),
        ("luxury",  "I prefer fewer, high-quality luxury items"),
        ("eco",     "Eco-friendly packaging and manufacturing are essential"),
        ("tech",    "I replace items frequently to stay up-to-date"),
        ("balanced",  "I buy items only when necessary or convenient"),
    ]

    q1 = forms.ChoiceField(label="When choosing a product, what's most important to you?", choices=Q1_CHOICES, widget=forms.RadioSelect)
    q2 = forms.ChoiceField(label="Which shopping habit best describes you?", choices=Q2_CHOICES, widget=forms.RadioSelect)
    q3 = forms.ChoiceField(label="What's your typical spending range per item?", choices=Q3_CHOICES, widget=forms.RadioSelect)
    q4 = forms.ChoiceField(label="Which sources do you trust most for shopping advice?", choices=Q4_CHOICES, widget=forms.RadioSelect)
    q5 = forms.ChoiceField(label="Which statement best describes your shopping philosophy?", choices=Q5_CHOICES, widget=forms.RadioSelect)

    def determine_persona(self):
        from collections import Counter

        votes = [
            self.cleaned_data["q1"],
            self.cleaned_data["q2"],
            self.cleaned_data["q3"],
            self.cleaned_data["q4"],
            self.cleaned_data["q5"],
        ]
        count = Counter(votes)
        max_votes = max(count.values())

        tied = [p for p, v in count.items() if v == max_votes]

        priority = ["tech", "eco", "luxury", "budget", "balanced"]

        for p in priority:
            if p in tied:
                return p

