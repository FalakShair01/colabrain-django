from django.shortcuts import render
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CompanySerializer, CompanyProfileSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Company
from rest_framework.parsers import MultiPartParser, FormParser



class RegisterCompany(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg': 'Registration successfull'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_201_CREATED)
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Password successfully changed."}, status=200)


class CompanyProfileView(RetrieveUpdateAPIView):
    serializer_class = CompanyProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)


    def get_object(self):
        return self.request.user.company
