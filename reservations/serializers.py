# reservations/serializers.py

from rest_framework import serializers
from .models import Reservation, ReservationDocument
from offers.models import Offer

# Molde para os documentos de cada reserva
class ReservationDocumentSerializer(serializers.ModelSerializer):
    # CORREÇÃO: Trocamos o campo padrão por um que constrói a URL completa.
    file = serializers.SerializerMethodField()

    class Meta:
        model = ReservationDocument
        fields = ('id', 'description', 'file')

    def get_file(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None

# Molde simplificado para a oferta associada a uma reserva
class OfferInReservationSerializer(serializers.ModelSerializer):
    # CORREÇÃO: Trocamos o campo padrão por um que constrói a URL completa.
    image = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ('title', 'subtitle', 'image')

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

# Molde principal para a Reserva
class ReservationSerializer(serializers.ModelSerializer):
    offer = OfferInReservationSerializer(read_only=True)
    documents = ReservationDocumentSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Reservation
        fields = (
            'id', 
            'reservation_code', 
            'status', 
            'status_display',
            'start_date', 
            'end_date', 
            'total_price', 
            'offer', 
            'documents'
        )