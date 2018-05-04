from django.conf.urls import url

from .views import UpdateModelDatailAPIView, UpdateModelListAPIView

urlpatterns = [
    url(r'^$', UpdateModelListAPIView.as_view()),
    url(r'^(?P<id>\d+)/$', UpdateModelDatailAPIView.as_view()),
    # url(r'^json/serie/detail$', SerializedDetailView.as_view()),
    # url(r'^json/serie/list$', SerializedListView.as_view())
]
