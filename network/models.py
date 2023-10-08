from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="username_post")
    content = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)

    def __str__(self):
        return f"User: {self.username} -- {self.content}"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="user_follower")
    user_being_followed = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="user_following")

    def __str__(self):
        return f"{self.follower} follow {self.user_being_followed}"

class Like(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="username_like")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_like")

    def __str__(self):
        return f"{self.username}"