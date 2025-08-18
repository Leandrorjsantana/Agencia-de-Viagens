# offers/serializers.py

from rest_framework import serializers
from .models import Offer

# -----------------------------------------------------------------------------
# Serializer COMPLETO para a página de detalhes pública (O QUE ESTAVA FALTANDO)
# -----------------------------------------------------------------------------
class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Formata todos os dados de uma oferta para serem exibidos na página
    de detalhes para o seu cliente.
    """
    class Meta:
        model = Offer
        # Inclui todos os campos do modelo Offer
        fields = '__all__'

# -----------------------------------------------------------------------------
# Serializer LEVE para o painel de admin (O QUE JÁ TÍNHAMOS)
# -----------------------------------------------------------------------------
class OfferForAdminSerializer(serializers.ModelSerializer):
    """
    Formata apenas os campos necessários para o script de autopreenchimento
    no painel de administração.
    """
    class Meta:
        model = Offer
        fields = ('price', 'start_date', 'end_date', 'offer_code')