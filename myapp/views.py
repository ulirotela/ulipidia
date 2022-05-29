# Create your views here.
import coreapi
from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.filters import BaseFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.models import Article, Tag
from myapp.serializer import ArticleSerializer, ArticleSearchSerializer


class ArticleAPIView(viewsets.GenericViewSet,
                     mixins.CreateModelMixin):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def create(self, request, *args, **kwargs):
        serializer = ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        article = Article.objects.create(title=serializer.validated_data['title'],
                                         body=serializer.validated_data['body'])
        article.save()
        for tag in serializer.validated_data['tag']:
            t = Tag.objects.create(article=article, tag_name=tag)
            t.save()
        return Response(ArticleSerializer(article, many=False).data, status.HTTP_201_CREATED)


class ArticleFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [coreapi.Field(
            name='search',
            location='query',
            type='string'
        )]


class ArticleSearchAPIView(viewsets.GenericViewSet,
                           mixins.ListModelMixin):
    queryset = Article.objects.all()
    serializer_class = ArticleSearchSerializer
    filter_backends = (ArticleFilterBackend,)

    def list(self, request, *args, **kwargs):
        articles = Article.objects.filter(
            Q(title__icontains=self.request.GET['search']) or Q(body__icontains=self.request.GET['search']))
        tags = []
        for article in articles:
            for tag in Tag.objects.filter(article=article):
                if tag.tag_name not in tags:
                    tags.append(tag.tag_name)

        matched = Article.objects.none()
        for tag in tags:
            matched = Article.objects.filter(tag__tag_name=tag) | matched
        obj = {'matched_documents': articles,
               'related_documents': matched.distinct()}
        return Response(ArticleSearchSerializer(obj, many=False).data)


class DetailArticleApiView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def list(self, request, slug=None, *args, **kwargs):
        try:
            return Response(ArticleSerializer(Article.objects.get(slug=slug), many=False).data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
