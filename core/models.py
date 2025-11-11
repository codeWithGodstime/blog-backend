from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField
from drf_starter.storage_backends import PublicMediaStorage

from .manager import CustomUserManager


def upload_to(instance, filename):
    return f'avatars/{filename}'


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(storage=PublicMediaStorage(), upload_to=upload_to, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    school_attended = models.CharField(max_length=255, blank=True, null=True)
    social_links = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.username


# 🗂️ NEW: Folder model for organizing art
class ArtFolder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="art_folders")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "name")  # Prevent duplicate folder names per user
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.user.username})"


# 🎨 Artwork model
class ArtImage(models.Model):
    class Category(models.TextChoices):
        PAINTING = "Painting", "Painting"
        INSTALLATION = "Installation", "Installation"
        DIGITAL_ART = "Digital Art", "Digital Art"
        AI_ART = "AI Art", "AI Art"
        SCULPTURE = "Sculpture", "Sculpture"
        PRINTMAKING = "Printmaking", "Printmaking"
        EXPLORATIVE_ART = "Explorative Art", "Explorative Art"
        CERAMICS = "Ceramics", "Ceramics"
        DRAWING = "Drawing", "Drawing"
        PHOTOGRAPH = "Photograph", "Photograph"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="art_images")
    folder = models.ForeignKey('ArtFolder', on_delete=models.SET_NULL, null=True, blank=True, related_name="images")
    image = models.ImageField(storage=PublicMediaStorage(), upload_to="art_images/")
    title = models.CharField(max_length=255, blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True)
    category = models.CharField(
        max_length=50,
        choices=Category.choices,
        default=Category.PAINTING
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    size = models.CharField(max_length=100, blank=True, null=True)  # Size in bytes
    medium = models.CharField(max_length=100, blank=True, null=True)  # e.g., oil, acrylic, digital
    year_created = models.PositiveIntegerField(blank=True, null=True)  # Year the artwork was created

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        folder_name = self.folder.name if self.folder else "No Folder"
        return f"{self.title or 'Untitled'} ({self.category}) - {folder_name}"

class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    cover_image = models.ImageField(storage=PublicMediaStorage(), upload_to="blog_cover/", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(null=True)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="blog_posts"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.title.lower().replace(" ", "-")
        super().save(*args, **kwargs)
