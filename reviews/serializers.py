# reviews/serializers.py
from rest_framework import serializers
from .models import Review
from offers.models import Offer
from blog.serializers import AuthorSerializer 

class OfferInReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('id', 'title', 'destination_city')

class ReviewSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    offer = OfferInReviewSerializer(read_only=True)
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ('id', 'author', 'offer', 'title', 'content', 'rating', 'created_at', 'photo')

    def get_photo(self, obj):
        request = self.context.get('request')
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return None

# --- NOVO SERIALIZER PARA CRIAR UMA AVALIAÇÃO ---
class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        # Campos que o cliente irá enviar
        fields = ('offer', 'title', 'content', 'rating', 'photo')