# reviews/urls.py

from django.urls import path
from .views import ReviewListView, ReviewStatsView, MyReviewsView

urlpatterns = [
    # Rota para a lista pública de avaliações
    # GET /api/v1/reviews/list/
    path('list/', ReviewListView.as_view(), name='review_list'),

    # Rota para as estatísticas das avaliações
    # GET /api/v1/reviews/stats/
    path('stats/', ReviewStatsView.as_view(), name='review_stats'),

    # Rota para o cliente ver e criar as suas próprias avaliações
    # GET, POST /api/v1/reviews/my-reviews/
    path('my-reviews/', MyReviewsView.as_view(), name='my_reviews'),
]