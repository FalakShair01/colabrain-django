from django.urls import path
from .views import RegisterCompany, CompanyProfileUpdateView, CompanyProfileRetrieveView

urlpatterns = [
    path('register/', RegisterCompany.as_view()),
    path('company/profile/', CompanyProfileRetrieveView.as_view(), name='company-profile-retrieve'),
    path('company/profile/update/', CompanyProfileUpdateView.as_view(), name='company-profile-update')
]
