"""cfeapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

# from update.views import json_exemple_view, JsonCBV, SerializedDetailView, SerializedListView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/updates/', include('update.api.urls')),
    url(r'^api/pessoas/', include('pessoas.api.urls')),
    
#     url(r'^json/example/$', json_exemple_view),
#     url(r'^json/cbv/$', JsonCBV.as_view()),
#     url(r'^json/serie/detail$', SerializedDetailView.as_view()),
#     url(r'^json/serie/list$', SerializedListView.as_view())
]
