from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, generics
from .models import User
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .Utils import Utils
import jwt
import os
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password  # Import make_password to hash passwords
from django.contrib.auth import authenticate
from .serializers import (UserSerializer, ProfileSerializer, ChangePasswordSerializer, 
                          SendPasswordResetEmailSerializer, ResetPasswordSerializer, LoginSerializer)
from .token_utils import get_tokens_for_user
from .permissions import IsAdminOrSelf


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminOrSelf]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)
    
    # def create(self, request, *args, **kwargs):
    #     # Generate a random password for the user
    #     generated_password = User.objects.make_random_password()

    #     # Set the generated password in the request data
    #     request.data['password'] = generated_password

    #     # Use the serializer to create the user
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)

    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email').lower()
        password = serializer.data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                if user.is_verified:
                    token = get_tokens_for_user(user)
                    serializer = UserSerializer(user)
                    return Response({'user':serializer.data,'token': token,"Message":"Login Successfull"}, status=status.HTTP_200_OK)
                else:
                    return Response({"Message": "Please check your email to verify."})
            else:
                return Response({"Message": "User is not active. Please Contact to Support team."})
        else:
            return Response({"Message":"Email and Password is not valid"})


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]

    def get_object(self):
        return self.request.user


class RemoveUserProfile(APIView):
    def patch(self, request):
        instance=request.user
        serializer = ProfileSerializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            profile_path = instance.profile.path
            if profile_path and os.path.exists(profile_path):
                os.remove(profile_path)
        except Exception as e:
            instance.profile = ""
            serializer.save()
            return Response(serializer.data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({"Message": "Password Has been Changed"}, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):
    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({"Message": "Password Reset Email Send Successfully"}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    def post(self, request, uid, token):
        serializer = ResetPasswordSerializer(data=request.data, context={
                                             'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({"Message": "Password Has been Reset Successfully"}, status=status.HTTP_200_OK)


