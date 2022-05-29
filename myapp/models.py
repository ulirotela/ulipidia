from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify


class Article(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField(allow_unicode=True, editable=False)

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Article)
def store_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


class Tag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='tag')
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return self.tag_name
