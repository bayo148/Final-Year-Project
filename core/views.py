from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from.models import ChatMessage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def home(request):
    return render(request, 'core/home.html')

@csrf_exempt
@login_required
def chat_view(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")
        try:

            ChatMessage.objects.create(
                user=request.user,
                message=user_message,
                role='user'
            )


            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a helpful e-commerce shopping assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            bot_reply = response.choices[0].message.content

            # 3) Save the bot's reply in the DB
            ChatMessage.objects.create(
                user=request.user,
                message=bot_reply,
                role='bot'
            )

            return JsonResponse({'reply': bot_reply})
        except Exception as e:
            return JsonResponse({'reply': f"Error: {str(e)}"})

    # Handle GET requests: show existing chat messages
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




