from django.conf.urls import url, include

from .views import PessoaListApiView

urlpatterns = [
    url(r'^$', PessoaListApiView.as_view()),
    
#     url(r'^json/example/$', json_exemple_view),
#     url(r'^json/cbv/$', JsonCBV.as_view()),
#     url(r'^json/serie/detail$', SerializedDetailView.as_view()),
#     url(r'^json/serie/list$', SerializedListView.as_view())
]