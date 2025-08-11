# leads/urls.py

from django.urls import path
from .views import LeadCreateView

urlpatterns = [
    # O endereço será: /api/v1/leads/submit/
    path('submit/', LeadCreateView.as_view(), name='submit_lead'),
]