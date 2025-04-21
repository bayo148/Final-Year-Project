from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("chat/new/", views.new_chat, name="chat_new"),                # fresh conversation
    path("chat/<int:conversation_id>/", views.chat_view, name="chat_with_id"),
    path("chat/<int:conversation_id>/delete/", views.delete_conversation, name="delete_conversation"),
    # Keep original /chat/ URL – it redirects to the most‑recent conversation or creates one.
    path("chat/", views.chat_redirect_to_latest, name="chat"),

    path("accounts/login/",    views.login_view,    name="login"),
    path("accounts/register/", views.register_view, name="register"),
    path("accounts/logout/",   views.logout_view,   name="logout"),
    path("profile/",           views.profile_view,  name="profile"),
]

