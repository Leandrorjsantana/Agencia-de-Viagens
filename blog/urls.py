# blog/urls.py

from django.urls import path
from .views import (
    PostListView, 
    PostDetailView, 
    BlogSidebarDataView, 
    CommentListCreateView,
    CategoryPostListView # Importa a nova view
)

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('sidebar-data/', BlogSidebarDataView.as_view(), name='blog_sidebar_data'),
    path('posts/<slug:slug>/comments/', CommentListCreateView.as_view(), name='post_comments'),
    
    # --- NOVA ROTA ADICIONADA AQUI ---
    # Endereço para a lista de posts por categoria: /api/v1/blog/categoria/<slug-da-categoria>/
    path('categoria/<slug:category_slug>/', CategoryPostListView.as_view(), name='category_post_list'),
]