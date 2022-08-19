import io
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.Serializer):
    categoryType = serializers.CharField(read_only=True)
    dateCreation = serializers.DateTimeField(read_only=True)
    postCategory_id = serializers.IntegerField(read_only=True)
    # катерогии уже определено числовое значение id в моделе
    title = serializers.CharField(max_length=255)
    slug = serializers.SlugField(read_only=True)
    text = serializers.CharField()
    photo = serializers.ImageField(read_only=True)
    rating = serializers.IntegerField(default=0)
    status = serializers.CharField(read_only=True)

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.categoryType = validated_data.get(
            "categoryType", instance.categoryType)
        instance.postCategory_id = validated_data.get(
            "postCategory_id", instance.postCategory_id)
        instance.title = validated_data.get("title", instance.title)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.text = validated_data.get("text", instance.text)
        instance.photo = validated_data.get("photo", instance.photo)
        instance.rating = validated_data.get("rating", instance.rating)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance

    # <----------------REST процесс кодировани и декодирования JSON строки ------------------->

    # class PostModel:
    #     def __init__(self, title, text):
    #         self.title = title
    #         self.text = text

    # class PostSerializer(serializers.Serializer):
    #     title = serializers.CharField(max_length=255)
    #     text = serializers.CharField()

    # def encode():
    #     model = PostModel('HERE IS MY TITLE',
    #                       'Text: Here is the Text of the Article')
    #     model_sr = PostSerializer(model)
    #     print(model_sr.data, type(model_sr.data), sep='\n')
    #     json = JSONRenderer().render(model_sr.data)
    #     print(json, type(json), sep='\n')

    # def decode():
    #     stream = io.BytesIO(
    #         b'{"title":"HERE IS MY TITLE","text":"Text: Here is the Text of the Article"}')
    #     data = JSONParser().parse(stream)
    #     serializer = PostSerializer(data=data)
    #     serializer.is_valid()
    #     print(serializer.validated_data)
