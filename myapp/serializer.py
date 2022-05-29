from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from myapp.models import Article, Tag


class TagSerializer(serializers.Serializer):
    class Meta:
        model = Tag
        fields = ['tag_name']


class ArticleSerializer(ModelSerializer):
    tag = serializers.StringRelatedField(many=True)

    class Meta:
        model = Article
        fields = ['title', 'body', 'tag', 'slug']

    def to_internal_value(self, data):
        return data


class ArticleSearchSerializer(serializers.Serializer):
    matched_documents = ArticleSerializer(many=True)
    related_documents = ArticleSerializer(many=True)
