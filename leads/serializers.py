# leads/serializers.py

from rest_framework import serializers
from .models import Lead

class LeadCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criar uma nova Solicitação de Reserva (Lead)
    a partir do formulário do site.
    """
    class Meta:
        model = Lead
        # Lista dos campos que o nosso formulário do frontend irá enviar
        fields = (
            'offer',
            'full_name',
            'email',
            'phone_number',
            'travel_date',
            'number_of_people',
            'observations',
            'client_user',
        )