# help_center/urls.py

from django.urls import path
from .views import HelpCenterListView

urlpatterns = [
    # O endereço será: /api/v1/help-center/
    path('', HelpCenterListView.as_view(), name='help_center_list'),
]