from django.shortcuts import render
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
def chat_view(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a helpful e-commerce shopping assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            bot_reply = response.choices[0].message.content
            return JsonResponse({'reply': bot_reply})
        except Exception as e:
            return JsonResponse({'reply': f"Error: {str(e)}"})

    return render(request, 'core/chat.html')




