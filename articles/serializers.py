from rest_framework import serializers
from .models import Article,Comment


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"

class ArticleSerializer(ArticleDetailSerializer):
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        if len(obj.content) > 50:
            content = obj.content[:50] + '...'
        else:
            content = obj.content
        return  content
    
class CommentSerializer(serializers.ModelSerializer):
    article = serializers.CharField(source='article.title', read_only=True)

    class Meta:
        model= Comment
        fields=('article','content','created_at','updated_at')