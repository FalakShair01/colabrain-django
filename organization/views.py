from django.shortcuts import render
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrganizationSerializer

# Create your views here.


class Register(APIView):
    def post(self, request):
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'msg': 'Registration successfull'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_201_CREATED)

