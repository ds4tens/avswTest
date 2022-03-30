from rest_framework import generics
from result import serializers
# Create your views here.


class GoogleApiView(generics.CreateAPIView):
    serializer_class = serializers.GoogleSerializer

class CrawlerTestApiView(generics.CreateAPIView):
    serializer_class = serializers.CrawlerTestSerializer

class VKApiView(generics.CreateAPIView):
    serializer_class = serializers.VKSerializer

class YandexApiView(generics.CreateAPIView):
    serializer_class = serializers.YandexSerializer

class StackoverflowApiView(generics.CreateAPIView):
    serializer_class = serializers.StackoverflowSerializer