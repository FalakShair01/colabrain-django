from django.urls import path
from .views import RegisterCompany, ChangePasswordView, CompanyProfileView

urlpatterns = [
    path('register/', RegisterCompany.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('company-profile/', CompanyProfileView.as_view(), name='company-profile'),
    ]
