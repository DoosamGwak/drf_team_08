from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import Article, Comment, Image


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(use_url=True)

    class Meta:
        model = Image
        fields = (
            "id",
            "image_url",
        )


class ArticleDetailSerializer(serializers.ModelSerializer):
    image = ImageSerializer(many=True, read_only=True)
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

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)  # 기본 데이터를 가져옵니다.
    #     request = self.context.get("request")  # 요청 정보를 가져옵니다.
    #     if request and request.method == "GET":
    #         representation["content"] = self.get_content(instance)  # 가공된 content를 설정합니다.
    #         representation["images"] = self.get_image(instance)  # 가공된 image를 설정합니다.
    #     return representation  # 최종 데이터를 반환합니다.

    # def create(self, validated_data):
    #     images_data = validated_data.pop("images")
    #     print("111111111111111111111111111")
    #     article = Article.objects.create(**validated_data)
    #     print("22222222222222222222222222222222222")
    #     for image_data in images_data:
    #         Image.objects.create(article=article, image_url=image_data)
    #     return article


class CommentSerializer(serializers.ModelSerializer):
    article = serializers.CharField(source="article.title", read_only=True)

    class Meta:
        model = Comment
        fields = ("article", "content", "created_at", "updated_at")
