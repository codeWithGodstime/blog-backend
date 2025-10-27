from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ArtFolder, ArtImage, BlogPost
from .serializers import (
    ArtFolderSerializer,
    ArtImageSerializer,
    AuthenticationSerializer,
    BlogPostDetailSerializer,
    BlogPostListSerializer,
    UserSerializer,
)

User = get_user_model()


# --------------------------------------
# PAGINATION & PERMISSIONS
# --------------------------------------
class BlogPostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow only admins to create/update/delete. Everyone can read."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


# --------------------------------------
# AUTHENTICATION
# --------------------------------------
@extend_schema(tags=["Authentication"])
class AuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"])
    @transaction.atomic
    def register(self, request):
        serializer = AuthenticationSerializer.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response_serializer = UserSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = AuthenticationSerializer.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"detail": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({"detail": "User account is disabled"}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {"id": user.id, "email": user.email, "username": user.username},
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    def refresh(self, request):
        serializer = AuthenticationSerializer.RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh"]
        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            return Response({"access": str(access_token), "refresh": str(refresh)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Invalid refresh token", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def forget_password(self, request):
        serializer = AuthenticationSerializer.PasswordForgetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "If an account exists, you'll get an email"}, status=status.HTTP_200_OK)

        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"

        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password: {reset_link}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response({"detail": "If an account exists, you'll get an email"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def password_reset_confirm(self, request):
        serializer = AuthenticationSerializer.PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data["uid"]))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, OverflowError):
            return Response({"detail": "Invalid UID"}, status=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data["token"]
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"detail": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"detail": "Password reset successful"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        serializer = AuthenticationSerializer.ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data["current_password"]):
            return Response({"detail": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)


# --------------------------------------
# BLOG
# --------------------------------------
@extend_schema(tags=["Blog"])
class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all().order_by("-created_at")
    pagination_class = BlogPostPagination
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "list":
            return BlogPostListSerializer
        return BlogPostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# --------------------------------------
# USERS
# --------------------------------------
@extend_schema(tags=["Users"])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return User.objects.filter(is_superuser=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search = request.query_params.get("q")
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(username__icontains=search)
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get", "put"], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Retrieve or update the authenticated user's profile."""
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def my_artworks(self, request):
        """Get all artworks uploaded by the current user."""
        user = request.user
        artworks = ArtImage.objects.filter(user=user).order_by("-uploaded_at")
        serializer = ArtImageSerializer(artworks, many=True)
        return Response(serializer.data)


# --------------------------------------
# ART FOLDERS
# --------------------------------------
@extend_schema(tags=["Art Folders"])
class ArtFolderViewSet(viewsets.ModelViewSet):
    """
    Manage folders that group artworks for a user.
    """

    serializer_class = ArtFolderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show folders belonging to the current user
        return ArtFolder.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# --------------------------------------
# ART IMAGES
# --------------------------------------
@extend_schema(tags=["Art Images"])
class ArtImageViewSet(viewsets.ModelViewSet):
    """
    CRUD for artworks. Supports folder & category filtering.
    """

    serializer_class = ArtImageSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = ArtImage.objects.select_related("folder", "user").order_by("-uploaded_at")

        # Filtering
        category = self.request.query_params.get("category")
        folder_id = self.request.query_params.get("folder")
        user_id = self.request.query_params.get("user")

        if category:
            queryset = queryset.filter(category=category)
        if folder_id:
            queryset = queryset.filter(folder_id=folder_id)
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)