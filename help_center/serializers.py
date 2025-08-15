# help_center/serializers.py

from rest_framework import serializers
from .models import HelpCategory, HelpArticle

class HelpArticleSerializer(serializers.ModelSerializer):
    """ Serializer para um único artigo de ajuda (pergunta e resposta) """
    class Meta:
        model = HelpArticle
        fields = ('id', 'question', 'answer')

class HelpCategorySerializer(serializers.ModelSerializer):
    """ Serializer para uma categoria, incluindo todos os seus artigos aninhados """
    articles = HelpArticleSerializer(many=True, read_only=True)

    class Meta:
        model = HelpCategory
        fields = ('id', 'title', 'slug', 'icon_class', 'articles')