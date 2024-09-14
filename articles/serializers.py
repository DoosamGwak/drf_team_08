from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Article, Image


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

    class Meta:
        model = Article
        fields = "__all__"

    # 조회수 증가 로직
    def to_representation(self, instance):
        instance.hits += 1
        instance.save(update_fields=["hits"])
        return super().to_representation(instance)


class ArticleSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), required=False
    )  # Allow multiple images

    class Meta:
        model = Article
        fields = ["id", "title", "content", "images", "hits"]

    # 기사 리스트 내용 50자 이내로만 나오게 하는 로직
    def get_content(self, instance):
        request = self.context.get("request")  # 요청 정보를 가져옵니다.
        if request and request.method == "GET":  # GET 요청인지 확인합니다.
            if len(instance.content) > 50:  # 내용이 50자보다 길면
                return instance.content[:50] + "..."  # 50자까지 잘라서 반환합니다.
            return instance.content  # 그렇지 않으면 원본 내용을 반환합니다.
        return instance.content  # POST 요청일 때는 원본 내용을 그대로 반환합니다.

    # PK가 가장 낮은 이미지를 가져오는 로직
    def get_image(self, instance):
        request = self.context.get("request")  # 요청 정보를 가져옵니다.
        if request and request.method == "GET":  # GET 요청인지 확인합니다.
            # 가장 낮은 PK의 이미지를 가져옵니다.
            if instance.image.exists():
                lowest_pk_image = instance.image.order_by("id").first()
                return lowest_pk_image.image_url.url  # 이미지 URL 반환
        return None  # 이미지가 없으면 None을 반환

    def to_representation(self, instance):
        representation = super().to_representation(instance)  # 기본 데이터를 가져옵니다.
        request = self.context.get("request")  # 요청 정보를 가져옵니다.
        if request and request.method == "GET":
            representation["content"] = self.get_content(instance)  # 가공된 content를 설정합니다.
            representation["images"] = self.get_image(instance)  # 가공된 image를 설정합니다.
        return representation  # 최종 데이터를 반환합니다.

    def create(self, validated_data):
        images_data = validated_data.pop("images")
        article = Article.objects.create(**validated_data)
        for image_data in images_data:
            Image.objects.create(article=article, image_url=image_data)
        return article
