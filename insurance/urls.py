# insurance/urls.py
from django.urls import path
from .views import InsurancePageDataView

urlpatterns = [
    # O endereço será: /api/v1/insurance/page-data/
    path('page-data/', InsurancePageDataView.as_view(), name='insurance_page_data'),
]