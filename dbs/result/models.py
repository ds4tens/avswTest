from django.db import models

# Create your models here.

class GoogleSubUrls(models.Model):
    url = models.TextField(verbose_name='sub_url')

class Google(models.Model):
    base_url = models.URLField(verbose_name='base_url')
    sub_url = models.ForeignKey(to=GoogleSubUrls, verbose_name='sub_url', on_delete=models.CASCADE)
    depth = models.IntegerField(default=0)


class CrawlerTestSubUrls(models.Model):
    url = models.TextField(verbose_name='sub_url')

class CrawlerTest(models.Model):
    base_url = models.URLField(verbose_name='base_url')
    sub_url = models.ForeignKey(to=CrawlerTestSubUrls, verbose_name='sub_url', on_delete=models.CASCADE)
    depth = models.IntegerField(default=0)


class VKSubUrls(models.Model):
    url = models.TextField(verbose_name='sub_url')

class VK(models.Model):
    base_url = models.URLField(verbose_name='base_url')
    sub_url = models.ForeignKey(to=VKSubUrls, verbose_name='sub_url', on_delete=models.CASCADE)
    depth = models.IntegerField(default=0)


class YandexSubUrls(models.Model):
    url = models.TextField(verbose_name='sub_url')

class Yandex(models.Model):
    base_url = models.URLField(verbose_name='base_url')
    sub_url = models.ForeignKey(to=YandexSubUrls, verbose_name='sub_url', on_delete=models.CASCADE)
    depth = models.IntegerField(default=0)


class StackoverflowSubUrls(models.Model):
    url = models.TextField(verbose_name='sub_url')

class Stackoverflow(models.Model):
    base_url = models.URLField(verbose_name='base_url')
    sub_url = models.ForeignKey(to=StackoverflowSubUrls, verbose_name='sub_url', on_delete=models.CASCADE)
    depth = models.IntegerField(default=0)