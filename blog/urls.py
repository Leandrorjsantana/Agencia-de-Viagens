# blog/urls.py

from django.urls import path
from .views import PostListView, PostDetailView, BlogSidebarDataView, CommentListCreateView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('sidebar-data/', BlogSidebarDataView.as_view(), name='blog_sidebar_data'),
    
    # --- NOVA ROTA PARA OS COMENTÁRIOS ---
    # Endereço para listar e criar comentários: /api/v1/blog/posts/<slug-do-post>/comments/
    path('posts/<slug:slug>/comments/', CommentListCreateView.as_view(), name='post_comments'),
]