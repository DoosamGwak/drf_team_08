from rest_framework import serializers
from .models import Article


# class ImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Image
#         fields = ["id","image_url"]

#     def get_image_url(self, obj):
#         if obj.image_url:
#             return obj.image_url.url


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"

    # 조회수 증가 로직
    def to_representation(self, instance):
        instance.hits += 1
        instance.save(update_fields=["hits"])
        return super().to_representation(instance)


class ArticleSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = "__all__"

    # 기사 리스트 내용 50자 이내로만 나오게 하는 로직
    def get_content(self, instance):
        if len(instance.content) > 50:
            content = instance.content[:50] + "..."
        else:
            content = instance.content
        return content


# class ArticleCreateSerializer(serializers.ModelSerializer):
#     images=ImageSerializer()
#     class Meta:
#         model = Article
#         fields = "__all__"
