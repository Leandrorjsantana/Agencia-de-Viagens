# help_center/views.py

from rest_framework import generics, permissions
from .models import HelpCategory
from .serializers import HelpCategorySerializer

class HelpCenterListView(generics.ListAPIView):
    """
    View para listar todas as Categorias de Ajuda, com os seus
    artigos aninhados.
    """
    queryset = HelpCategory.objects.all().order_by('order')
    serializer_class = HelpCategorySerializer
    permission_classes = [permissions.AllowAny]