from rest_framework import serializers
from .models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        
    def create(self, validated_data):
        return Organization.objects.create_user(**validated_data)