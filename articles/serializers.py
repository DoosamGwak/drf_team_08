from rest_framework import serializers
from .models import Article,Comment,Image,Category



class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ("id", "category_name",)

class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(use_url=True)

    class Meta:
        model = Image
        fields = (
            "id",
            "image_url",
        )


class ArticleDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    reporter = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = "__all__"

    # 조회수 증가 로직
    def to_representation(self, instance):
        instance.hits += 1
        instance.save(update_fields=["hits"])
        return super().to_representation(instance)


class ArticleListSerializer(serializers.ModelSerializer):
    preview_content = serializers.SerializerMethodField(read_only=True)
    preview_image = serializers.SerializerMethodField(read_only=True)
    reporter = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Article
        fields = (
            "id", 
            "category",
            "title",
            "reporter",
            "preview_content",
            "preview_image",
            "hits",
        )

    # 기사 리스트 내용 50자 이내로만 나오게 하는 로직
    def get_preview_content(self, instance):
        content = instance.content
        instance.preview_content = (
            (content[:50] + "...") if len(content) > 50 else content
        )  # 내용이 50자보다 길면 50자까지 잘라서 반환합니다.
        return instance.preview_content

    # PK가 가장 낮은 이미지를 가져오는 로직
    def get_preview_image(self, instance):
        if instance.images.exists():
            lowest_pk_image = instance.images.order_by("id").first()
            return lowest_pk_image.image_url.url  # 이미지 URL 반환
        return None  # 이미지가 없으면 None을 반환


class ArticleCreateSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)
    reporter = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "category",
            "content",
            "images",
            "reporter",
            "hits",
        )
        write_only_fields = ("content",)

    def get_images(self, instance):
        if instance.images.exists():
            return list(
                instance.images.values_list("image_url", flat=True)
            )  # 이미지 URL 반환
        return None  # 이미지가 없으면 None을 반환


class CommentSerializer(serializers.ModelSerializer):
    article = serializers.CharField(source="article.title", read_only=True)
    commentor = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = ("article", "commentor", "content", "created_at", "updated_at")
