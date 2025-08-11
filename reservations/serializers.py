# reservations/serializers.py

from rest_framework import serializers
from .models import Reservation, ReservationDocument
from offers.models import Offer

class ReservationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationDocument
        fields = ('id', 'description', 'file', 'uploaded_by')

class OfferInReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('title', 'subtitle', 'image')

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

# --- CLASSE QUE FALTAVA ADICIONADA AQUI ---
class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        # Campos que o frontend irá enviar ao criar uma reserva
        fields = ('offer', 'start_date', 'end_date', 'total_price', 'notes')

# --- CLASSE QUE TAMBÉM ERA NECESSÁRIA PARA O UPLOAD ---
class ReservationDocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationDocument
        fields = ('description', 'file')