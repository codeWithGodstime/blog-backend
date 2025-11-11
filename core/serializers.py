import logging
from typing import Dict, Any
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as SimpleJWTTokenObtainPairSerializer
from .models import BlogPost, ArtImage, ArtFolder

User = get_user_model()
logger = logging.getLogger(__file__)


# -----------------------------
# AUTHENTICATION SERIALIZERS
# -----------------------------
class AuthenticationSerializer:
    class RegisterSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ["username", "email", "password"]
            extra_kwargs = {"password": {"write_only": True}}

        def validate_password(self, value):
            from django.contrib.auth.password_validation import validate_password
            validate_password(value)
            return value

        def create(self, validated_data):
            return User.objects.create_user(
                username=validated_data["username"],
                email=validated_data["email"],
                password=validated_data["password"],
            )

    class LoginSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(write_only=True)

    class RefreshTokenSerializer(serializers.Serializer):
        refresh = serializers.CharField()

    class PasswordForgetSerializer(serializers.Serializer):
        email = serializers.EmailField()

    class PasswordResetConfirmSerializer(serializers.Serializer):
        new_password = serializers.CharField(write_only=True)
        token = serializers.CharField()
        uid = serializers.CharField()

        def validate_new_password(self, value):
            from django.contrib.auth.password_validation import validate_password
            validate_password(value)
            return value

    class ChangePasswordSerializer(serializers.Serializer):
        current_password = serializers.CharField(write_only=True)
        new_password = serializers.CharField(write_only=True)

        def validate_new_password(self, value):
            from django.contrib.auth.password_validation import validate_password
            validate_password(value)
            return value


# -----------------------------
# TOKEN SERIALIZER
# -----------------------------
class TokenObtainSerializer(SimpleJWTTokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]):
        data = super().validate(attrs)
        user = self.user
        user_data = UserSerializer(user).data
        data["data"] = user_data
        return data


# -----------------------------
# BLOG SERIALIZERS
# -----------------------------
class BlogPostListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = BlogPost
        fields = ["id", "title", "slug", 'except' "author_name", "excerpt", "created_at"]


class BlogPostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "title",
            "slug",
            "cover_image",
            "content",
            "author",
            "author_name",
            "category",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "author_name", "created_at", "updated_at"]


# -----------------------------
# USER SERIALIZER
# -----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "username", "email", "bio", "avatar",
            "dob", "city", "country", "school_attended", "social_links"
        ]
        read_only_fields = ["id", "email", "username"]


# -----------------------------
# ART SERIALIZERS
# -----------------------------
class ArtFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtFolder
        fields = ["id", "name", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ArtImageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    bio = serializers.CharField(source="user.bio", read_only=True)
    folder = ArtFolderSerializer(read_only=True)
    folder_id = serializers.PrimaryKeyRelatedField(
        queryset=ArtFolder.objects.all(),
        source="folder",
        write_only=True,
        required=False,
        allow_null=True,
    )
    category_display = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = ArtImage
        fields = [
            "id",
            "year_created",
            "medium",
            "size",
            "user",
            "username",
            "bio",
            "title",
            "image",
            "caption",
            "folder",
            "folder_id",
            "category",
            "category_display",
            "uploaded_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "uploaded_at", "updated_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
