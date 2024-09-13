from rest_framework import serializers
from .models import Article, Image

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Image
        fields = ("id","image",)


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
    images = serializers.ListField(
        child=serializers.ImageField(), required=False
    )  # Allow multiple images

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'images']

    # 기사 리스트 내용 50자 이내로만 나오게 하는 로직
    def get_content(self, instance):
        if len(instance.content) > 50:
            content = instance.content[:50] + "..."
        else:
            content = instance.content
        return content

    def create(self, validated_data):
        images_data = validated_data.pop("images",[])
        print(images_data,"1"*30)
        article = Article.objects.create(**validated_data)
        for image_data in images_data:
            print(image_data,"3"*30)
            Image.objects.create(article=article, image_url=image_data)
        print("4"*30)
        return article

    # def create(self, validated_data):
    #     instance = Article.objects.create(**validated_data)
    #     print(type(self.data),"1"*30)
    #     image_set = self.data["request"]
    #     for image_data in image_set.getlist("image"):
    #         Image.objects.create(article=instance, image=image_data)
    #     return instance
