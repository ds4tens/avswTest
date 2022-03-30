from rest_framework import serializers
from result import models

class GoogleSerializer(serializers.ModelSerializer):

    sub_url = serializers.CharField()

    class Meta:
        model = models.Google
        fields = ('base_url', 'sub_url', 'depth', )

    def create(self, validated_data):
        sub_url = models.GoogleSubUrls(url=validated_data.get('sub_url'))
        sub_url.save()

        url = models.Google(base_url=validated_data.get('base_url'), sub_url=sub_url, depth=validated_data.get('depth'))
        url.save()
        return url


class CrawlerTestSerializer(serializers.ModelSerializer):

    sub_url = serializers.CharField()

    class Meta:
        model = models.CrawlerTest
        fields = ('base_url', 'sub_url', 'depth', )

    def create(self, validated_data):
        sub_url = models.CrawlerTestSubUrls(url=validated_data.get('sub_url'))
        sub_url.save()

        url = models.CrawlerTest(base_url=validated_data.get('base_url'), sub_url=sub_url, depth=validated_data.get('depth'))
        url.save()
        return url

class VKSerializer(serializers.ModelSerializer):

    sub_url = serializers.CharField()

    class Meta:
        model = models.VK
        fields = ('base_url', 'sub_url', 'depth', )

    def create(self, validated_data):
        sub_url = models.VKSubUrls(url=validated_data.get('sub_url'))
        sub_url.save()

        url = models.VK(base_url=validated_data.get('base_url'), sub_url=sub_url, depth=validated_data.get('depth'))
        url.save()
        return url


class YandexSerializer(serializers.ModelSerializer):

    sub_url = serializers.CharField()

    class Meta:
        model = models.Yandex
        fields = ('base_url', 'sub_url', 'depth', )

    def create(self, validated_data):
        sub_url = models.YandexSubUrls(url=validated_data.get('sub_url'))
        sub_url.save()

        url = models.Yandex(base_url=validated_data.get('base_url'), sub_url=sub_url, depth=validated_data.get('depth'))
        url.save()
        return url

class StackoverflowSerializer(serializers.ModelSerializer):

    sub_url = serializers.CharField()

    class Meta:
        model = models.Stackoverflow
        fields = ('base_url', 'sub_url', 'depth', )

    def create(self, validated_data):
        sub_url = models.StackoverflowSubUrls(url=validated_data.get('sub_url'))
        sub_url.save()

        url = models.Stackoverflow(base_url=validated_data.get('base_url'), sub_url=sub_url, depth=validated_data.get('depth'))
        url.save()
        return url

