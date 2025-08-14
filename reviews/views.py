# reviews/views.py
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg, Count
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer # Adicionado o novo serializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.filter(is_approved=True)
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ['rating']
    search_fields = ['title', 'content', 'offer__destination_city']

class ReviewStatsView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, *args, **kwargs):
        approved_reviews = Review.objects.filter(is_approved=True)
        total_reviews = approved_reviews.count()
        average_rating = approved_reviews.aggregate(Avg('rating'))['rating__avg'] or 0.0
        satisfied_count = approved_reviews.filter(rating__in=[4, 5]).count()
        satisfied_percentage = (satisfied_count / total_reviews * 100) if total_reviews > 0 else 0
        data = {
            'total_reviews': total_reviews,
            'average_rating': round(average_rating, 1),
            'satisfied_percentage': round(satisfied_percentage),
        }
        return Response(data)

# --- NOVA VIEW PARA O CLIENTE CRIAR E VER AS SUAS AVALIAÇÕES ---
class MyReviewsView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewSerializer

    def get_queryset(self):
        # Retorna apenas as avaliações do utilizador logado
        return Review.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        # Associa a nova avaliação ao utilizador logado e aguarda aprovação
        serializer.save(author=self.request.user, is_approved=False)