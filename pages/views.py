# pages/views.py

from rest_framework import generics, permissions
from .models import Page
from .serializers import PageSerializer

class PageDetailView(generics.RetrieveAPIView):
    """
    View para obter os detalhes de uma página específica (como 'quem-somos') pelo seu slug.
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]