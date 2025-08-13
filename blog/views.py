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

# --- NOVA VIEW ADICIONADA AQUI ---
class CategoryPostListView(generics.ListAPIView):
    """
    View para listar todos os posts de uma categoria específica.
    """
    serializer_class = PostListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Pega o 'slug' da categoria a partir da URL
        category_slug = self.kwargs.get('category_slug')
        # Filtra e retorna apenas os posts que são daquela categoria E que estão publicados.
        return Post.objects.filter(category__slug=category_slug, is_published=True)

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

class CommentListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer

    def get_queryset(self):
        post_slug = self.kwargs.get('slug')
        return Comment.objects.filter(post__slug=post_slug, is_approved=True, parent__isnull=True)

    def perform_create(self, serializer):
        post_slug = self.kwargs.get('slug')
        post = Post.objects.get(slug=post_slug)
        serializer.save(author=self.request.user, post=post)