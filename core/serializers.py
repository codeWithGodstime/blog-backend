import logging
from typing import Dict, Any
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as SimpleJWTTokenObtainPairSerializer
from .models import BlogPost, ArtImage


User = get_user_model()
logger = logging.getLogger(__file__)


class AuthenticationSerializer:
    class RegisterSerializer(serializers.ModelSerializer):

        class Meta:
            model = User
            fields = [
                "email",
                "password",
            ]
            extra_kwargs = {"password": {"write_only": True}}

        def validate_password(self, value):
            from django.contrib.auth.password_validation import validate_password

            validate_password(value)
            return value

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


class TokenObtainSerializer(SimpleJWTTokenObtainPairSerializer):
 
     def validate(self, attrs: Dict[str, Any]):
 
         data = super().validate(attrs)
         user = self.user
         user_data = UserSerializer.UserRetrieveSerializer(user).data
         data['data'] = user_data
         return data


class BlogPostListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)
    excerpt = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "title",
            "slug",
            "author_name",
            "excerpt",
            "created_at",
        ]

    def get_excerpt(self, obj):
        # Take first 200 characters of content as preview
        return obj.content[:200] + ("..." if len(obj.content) > 200 else "")


class BlogPostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "author",
            "author_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "author_name", "created_at", "updated_at"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "bio", "avatar"]
        read_only_fields = ["id", "email", "username"]  # email & username fixed after registration


class ArtImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtImage
        fields = ["id", "user", "image", "caption", "uploaded_at", "updated_at"]
        read_only_fields = ["id", "user", "uploaded_at", "updated_at"]

    def create(self, validated_data):
        # Ensure uploaded image is tied to the current user
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)