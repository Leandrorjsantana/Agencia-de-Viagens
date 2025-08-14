# company_info/views.py

from rest_framework import generics, permissions
from .models import TeamMember
from .serializers import TeamMemberSerializer

class TeamMemberListView(generics.ListAPIView):
    """
    View para listar todos os membros da equipa.
    """
    queryset = TeamMember.objects.all().order_by('order')
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.AllowAny]