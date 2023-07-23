from rest_framework import serializers
from .models import Company
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


# class ChangePasswordSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     confirm_password = serializers.CharField(write_only=True)
#     class Meta:
#         model = User
#         fields = ['email', 'username', 'password', 'confirm_password']





# class CompanyProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = Company
#         fields = ['user', 'company_name', 'phone', 'profile_pic', 'role']

#     def update(self, instance, validated_data):
#         instance.company_name = validated_data.get('company_name', instance.company_name)
#         user_data = validated_data.get('user')
#         user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
#         if user_serializer.is_valid():
#             user_serializer.save()
#         instance.save()
#         return instance