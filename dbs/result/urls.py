from django.urls import path
from result import views


urlpatterns = [
    path('google/', views.GoogleApiView.as_view()),
    path('crawler-test/', views.CrawlerTestApiView.as_view()),
    path('yandex/', views.YandexApiView.as_view()),
    path('vk/', views.VKApiView.as_view()),
    path('stackoverflow/', views.StackoverflowApiView.as_view()),
]
