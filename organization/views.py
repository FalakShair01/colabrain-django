from django.shortcuts import render
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CompanySerializer, CompanyProfileSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Company


# Create your views here.


class RegisterCompany(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'msg': 'Registration successfull'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_201_CREATED)
    

# class ChangePasswordView(APIView):
#     def get(self, request):
#         serializer = ChangePasswordSerializer(data=request.data)



# class CompanyProfileRetrieveView(RetrieveAPIView):
#     queryset = Company.objects.all()
#     serializer_class = CompanyProfileSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user.company

# class CompanyProfileUpdateView(UpdateAPIView):
#     queryset = Company.objects.all()
#     serializer_class = CompanyProfileSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user.company
    
#     def perform_update(self, serializer):
#         serializer.save(user=self.request.user.company.user, partial=True)