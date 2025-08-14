# reviews/filters.py
from django_filters import rest_framework as filters
from .models import Review

class ReviewFilter(filters.FilterSet):
    # Permite a busca por palavra-chave no título ou conteúdo
    search = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Review
        # Define os campos pelos quais podemos filtrar
        fields = ['rating', 'search']