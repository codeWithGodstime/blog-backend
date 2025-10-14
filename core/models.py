from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import CustomUserManager

def upload_to(instance, filename):
    return 'avatars/{filename}'.format(filename=filename)


class User(AbstractUser):

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to=upload_to, blank=True, null=True)


class ArtImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="art_images")
    image = models.ImageField(upload_to="art_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    caption = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Image {self.id} by {self.user.username}"
    

class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.title.lower().replace(" ", "-")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title