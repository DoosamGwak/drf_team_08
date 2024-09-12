from rest_framework import serializers
from .models import Article


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