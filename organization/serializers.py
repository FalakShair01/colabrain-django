from rest_framework import serializers
from .models import Company
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model


User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs={
            'password':{'write_only':True}
        }
        
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(write_only=True)
    class Meta:
        model= Company
        fields = ['user', 'company_name', 'phone', 'profile_pic', 'role']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User(
            email=user_data['email'],
            username=user_data['username']
        )
        user.set_password(user_data['password'])
        user.save()

        company = Company.objects.create(user=user, **validated_data)
        return company


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        # Check if the new password and confirm new password match
        if new_password != confirm_password:
            raise serializers.ValidationError("New passwords and Comfirm Password do not match.")

        # Get the user from the request context
        user = self.context.get('user')

        # Check if the old password matches the password in the database
        if not check_password(old_password, user.password):
            raise serializers.ValidationError("Invalid old password.")
        
        #update the user's password
        user.set_password(new_password)
        user.save()

        return data



class UserEmailValidatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']
        extra_kwargs = {'email': {'validators': []}}  # Exclude email from unique constraint check


class CompanyProfileSerializer(serializers.ModelSerializer):
    user = UserEmailValidatorSerializer()
    profile_pic = serializers.ImageField(required=False)

    class Meta:
        model = Company
        fields = ['user' , 'company_name', 'country', 'phone', 'role','profile_pic']
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.country = validated_data.get('country', instance.country)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.role = validated_data.get('role', instance.role)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)

        # Update user fields individually without triggering the unique constraint check on email
        user = instance.user
        user.email = user_data.get('email', user.email)
        user.username = user_data.get('username', user.username)
        user.save()

        instance.save()
        return instance
    