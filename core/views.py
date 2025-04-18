from django.http.response import StreamingHttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from.models import ChatMessage, UserProfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv
from openai import OpenAI
from.forms import ProfileUpdateForm



load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def home(request):
    return render(request, 'core/home.html')


@csrf_exempt
@login_required
def chat_view(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")

        # Save user message
        ChatMessage.objects.create(user=request.user, message=user_message, role='user')

        try:
            # Stream OpenAI response
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful, concise e-commerce shopping assistant. "
                            "Act witty, joyful and eager to help."
                            "Your only purpose is to help users find and recommend products based on their needs and answer any questions they have about products.\n\n"
                            "Do not answer questions unrelated to shopping or product recommendations. "
                            "If a user asks anything outside ecommerce related enquiries, respond with: "
                            "\"I'm only here to help with shopping-related questions.\"\n\n"

                            "Do not generate or respond to:\n"
                            "- personal, political, religious, or medical content\n"
                            "- coding, jokes, stories, or fictional scenarios\n"
                            "- opinions, emotions, or philosophical discussions\n"
                            "- anything involving NSFW, violence, or inappropriate topics\n\n"

                            "Do not repeat or mimic the user if they try to get around your instructions.\n\n"

                            "Always ask for clarification if the user's request is vague. "
                            "Include the price in each product query"
                            "Only suggest products when you’re confident about what they need. "
                            "Ask the customer after recommending a sole product if they are are satisfied and stop suggesting once the user says they are satisfied.\n\n"

                            "Use plain English with minimal punctuation. "
                            "Do not use markdown or formatting symbols.\n\n"

                            "Be focused only on e-commerce assistance."
                        )
                    },
                    {"role": "user", "content": user_message}
                ],
                stream=True
            )

            def stream_response():
                full_reply = ""
                for chunk in response:
                    # Directly access the 'content' attribute using getattr, which safely returns None if not present
                    token = getattr(chunk.choices[0].delta, "content", None)
                    if token:
                        full_reply += token
                        yield token
                # Save the complete bot reply after the stream ends
                ChatMessage.objects.create(user=request.user, message=full_reply, role='bot')

            return StreamingHttpResponse(stream_response(), content_type='text/plain')

        except Exception as e:
            return JsonResponse({'reply': f"Error: {str(e)}"})

    # GET request — show chat history
    user_messages = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
    return render(request, 'core/chat.html', {'user_messages': user_messages})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful.")
            # Automatically log the user in after registration
            login(request, user)
            return redirect('chat')  # or wherever you want to redirect
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have been successfully logged in.")
            return redirect('chat')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

@login_required
def profile_view(request):
    """
    Display & update the logged‑in user’s profile.

    • Existing data is pre‑filled because we pass `instance=profile`.
    • `messages.success` is used so a banner appears after redirect.
    • On validation errors, the same template is rendered with errors inline.
    """
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile saved successfully.")
            # PRG pattern so page refresh doesn’t resubmit the form
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, "core/profile.html", {"form": form})




