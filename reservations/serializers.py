# reservations/serializers.py

from rest_framework import serializers
from .models import Reservation, ReservationDocument
from offers.models import Offer
from blog.serializers import AuthorSerializer # Reutilizado para consistência

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

class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('offer', 'start_date', 'end_date', 'total_price', 'notes')

class ReservationDocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationDocument
        fields = ('description', 'file')

class ReservationForReviewSerializer(serializers.ModelSerializer):
    offer_title = serializers.CharField(source='offer.title', read_only=True)
    # Precisamos do ID da oferta para associar a avaliação
    offer_id = serializers.IntegerField(source='offer.id', read_only=True)

    class Meta:
        model = Reservation
        fields = ('id', 'offer_title', 'offer_id')
