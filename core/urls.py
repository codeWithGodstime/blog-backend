from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
     TokenBlacklistView,
 )
from .views import AuthViewSet, BlogPostViewSet, UserViewSet, ArtImageViewSet

router = DefaultRouter()
router.register("auth", AuthViewSet, basename="auth")
router.register("posts", BlogPostViewSet, basename="posts")
router.register("users", UserViewSet, basename="user")
router.register("art-images", ArtImageViewSet, basename="artimage")

urlpatterns = [
     path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
] + router.urls