from rest_framework import serializers
from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .Utils import Utils
from django.conf import settings
from django.template.loader import render_to_string

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "phone", "address", "password", "role", "is_active", "created_at"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "phone", "address", "profile"]


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError(
                "Password and confirm password doesn't match")

        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        request = self.context.get('request')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            frontend_domain = settings.FRONTEND_DOMAIN
            # url = reverse('reset-password')
            link = frontend_domain + reverse('reset-password', args=[uid, token])
            # link = 'http://'+domain+'/api/user/reset-password/'+uid+'/'+token
            try: 
                # email_body = render_to_string(
                #     'emails/verify_email.html', {'title': 'Reset Password','username': user.username, 'absUrl': link, 'message': 'We received a request to reset your password for your Fastighetsvyn account. To create a new password, click on the following link:', 'endingMessage': "If you didn't request this change, please contact our support team immediately.", "btn": "Change Password"})
                # data = {
                #     'body': email_body,
                #     'subject': "Reset Password",
                #     'to': user.email,
                # }

                data = {
                    "subject": "Reset Password",
                    "body": f"Please click the link to Reset Your Password {link}",
                    "to": email
                }
                Utils.send_email(data)
                return attrs
            except Exception as e:
                return serializers.ValidationError({"Error": str(e)})

        else:
            raise serializers.ValidationError("No User found with this Email.")


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uid = self.context.get('uid')
        token = self.context.get('token')
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confrim Password doesn't match.")

        id = urlsafe_base64_decode(smart_str(uid))
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("Invalid Token")

        user.set_password(password)
        user.is_verified = True
        user.save()

        return attrs
