# company_info/urls.py

from django.urls import path
from .views import TeamMemberListView

urlpatterns = [
    # O endereço será: /api/v1/company-info/team/
    path('team/', TeamMemberListView.as_view(), name='team_member_list'),
]