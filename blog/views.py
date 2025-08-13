# blog/views.py

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from .models import Post, Category, BlogAdBanner, Comment
from .serializers import (
    PostListSerializer, PostDetailSerializer, BlogSidebarSerializer,
    CommentSerializer, CommentCreateSerializer
)
from rest_framework_simplejwt.authentication import JWTAuthentication

class PostListView(generics.ListAPIView):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostListSerializer
    permission_classes = [permissions.AllowAny]

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

class BlogSidebarDataView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, *args, **kwargs):
        recent_posts = Post.objects.filter(is_published=True).order_by('-published_at')[:5]
        categories = Category.objects.annotate(post_count=Count('post')).filter(post_count__gt=0).order_by('-post_count')
        ad_banners = BlogAdBanner.objects.filter(is_active=True)
        data = {
            'recent_posts': recent_posts,
            'categories': categories,
            'ad_banners': ad_banners,
        }
        serializer = BlogSidebarSerializer(data, context={'request': request})
        return Response(serializer.data)

# --- NOVA VIEW PARA LISTAR E CRIAR COMENTÁRIOS ---
class CommentListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    # Qualquer pessoa pode ver os comentários, mas só utilizadores logados podem criar
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        # Se o pedido for para criar (POST), usa o molde simples
        if self.request.method == 'POST':
            return CommentCreateSerializer
        # Se for para listar (GET), usa o molde completo com as respostas
        return CommentSerializer

    def get_queryset(self):
        # Filtra os comentários pelo slug do post que vem da URL
        # e pega apenas os comentários principais (que não são respostas)
        post_slug = self.kwargs.get('slug')
        return Comment.objects.filter(post__slug=post_slug, is_approved=True, parent__isnull=True)

    def perform_create(self, serializer):
        # Quando um novo comentário é criado, associa-o automaticamente
        # ao post correto e ao utilizador que está logado
        post_slug = self.kwargs.get('slug')
        post = Post.objects.get(slug=post_slug)
        serializer.save(author=self.request.user, post=post)