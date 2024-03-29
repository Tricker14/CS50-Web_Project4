
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("unfollow/<int:user_id>", views.unfollow, name="unfollow"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("new_post", views.new_post, name="new_post"),

    # API Route
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("is_like/<int:post_id>", views.is_like, name="is_like"),
    path("toggle_like/<int:post_id>", views.toggle_like, name="toggle_like"),
]
