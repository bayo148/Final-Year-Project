from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("chat/new/", views.new_chat, name="chat_new"),                # fresh conversation
    path("chat/<int:conversation_id>/", views.chat_view, name="chat_with_id"),
    path("chat/<int:conversation_id>/delete/", views.delete_conversation, name="delete_conversation"),
    path("chat/", views.chat_redirect_to_latest, name="chat"),

    path("accounts/login/",    views.login_view,    name="login"),
    path("accounts/register/", views.register_view, name="register"),
    path("accounts/logout/",   views.logout_view,   name="logout"),
    path("profile/",           views.profile_view,  name="profile"),

    path("persona/quiz/",   views.persona_quiz_view,   name="persona_quiz"),
    path("persona/result/", views.persona_result_view, name="persona_result"),
    path("persona/reset/",  views.reset_persona,       name="reset_persona"),
]

