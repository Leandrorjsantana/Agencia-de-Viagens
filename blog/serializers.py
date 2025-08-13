# blog/serializers.py

from rest_framework import serializers
from .models import Post, Category, Tag, BlogAdBanner, Comment
from django.contrib.auth.models import User

class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('full_name',)
    def get_full_name(self, obj):
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        return obj.username

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'slug')

class PostListSerializer(serializers.ModelSerializer):
    """
    Serializer para a lista de posts (versão simplificada).
    """
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Post
        # --- CORREÇÃO AQUI: Adicionando 'is_pinned' à lista de campos ---
        fields = ('id', 'title', 'slug', 'featured_image', 'summary', 'published_at', 'author', 'category', 'is_pinned')

class PostDetailSerializer(serializers.ModelSerializer):
    """
    Serializer para os detalhes de um único post (versão completa).
    """
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    related_posts = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'category', 'tags',
            'featured_image', 'summary', 'content', 'is_published',
            'is_pinned', 'published_at', 'updated_at', 'related_posts'
        ]

    def get_related_posts(self, obj):
        if not obj.category:
            return []
        
        related_posts_queryset = Post.objects.filter(
            category=obj.category, 
            is_published=True
        ).exclude(pk=obj.pk)[:4]
        
        return PostListSerializer(related_posts_queryset, many=True, context=self.context).data

# --- O resto dos seus serializers continua igual ---
class BlogAdBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogAdBanner
        fields = ('image', 'link_url')

class ReplySerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'created_at')

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    replies = ReplySerializer(many=True, read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'created_at', 'parent', 'replies')

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content', 'parent')

class RecentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'featured_image')

class CategoryWithCountSerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField()
    class Meta:
        model = Category
        fields = ('name', 'slug', 'post_count')

class BlogSidebarSerializer(serializers.Serializer):
    recent_posts = RecentPostSerializer(many=True)
    categories = CategoryWithCountSerializer(many=True)
    ad_banners = BlogAdBannerSerializer(many=True)
