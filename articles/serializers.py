from rest_framework import serializers
from .models import Article, Image


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Image
        fields = "__all__"


class ArticleDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = "__all__"

    # 조회수 증가 로직
    def to_representation(self, instance):
        instance.hits += 1
        instance.save(update_fields=["hits"])
        return super().to_representation(instance)

    # 모든 이미지 보이기 로직
    def get_images(self, instance):
        all_images = Image.objects.all()
        return ImageSerializer(all_images, many=True).data


class ArticleSerializer(serializers.ModelSerializer):
    # content = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

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

    # def create(self, validated_data):
    #     print("create시작")
    #     print(validated_data)
    #     images_data = validated_data.pop("images", [])  # 이미지 데이터 분리
    #     article = Article.objects.create(**validated_data)  # 기사 생성
    #     for image_data in images_data:  # 이미지 생성 후 연결
    #         print(image_data)
    #         image = Image.objects.create(**image_data)
    #         image.article = article
    #     return article
    def get_images(self, obj):
        image = obj.image.all()
        return ImageSerializer(instance=image, many=True, context=self.context).data

    def create(self, validated_data):
        instance = Article.objects.create(**validated_data)
        print(self.request)
        image_set = self.request.FILES
        for image_data in image_set.getlist("images"):
            Image.objects.create(article=instance, image=image_data)
        return instance
