from django.urls import path, include
from .views import (ProfileView, ChangePasswordView, 
                    SendPasswordResetEmailView, ResetPasswordView, LoginView, RemoveUserProfile, UserViewset)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user/management', UserViewset, basename='user-management')

urlpatterns = [
    path("user/login/", LoginView.as_view(), name="login"),
    path("user/profile/", ProfileView.as_view(), name="profile"),
    path("user/remove-profile/", RemoveUserProfile.as_view(), name="remove-profile"),
    path("user/change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("user/reset-password-email/", SendPasswordResetEmailView.as_view(), name="reset-password-email"),
    path(r"user/reset-password/<uid>/<token>/", ResetPasswordView.as_view(), name="reset-password"),
    path('', include(router.urls)),
]
