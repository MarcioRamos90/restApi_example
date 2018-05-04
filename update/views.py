import json
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.views.generic import View

from cfeapi.mixins import JsonResponseMixin
from .models import Update


def json_exemple_view(request):
    data = {
        'count': 2000,
        'content': 'some new content'
    }
    json_data = json.dumps(data)
    # return JsonResponse(data)
    return HttpResponse(json_data, content_type='application/json')


class JsonCBV(JsonResponseMixin, View):
    def get(self, request, *args, **kwargs):
        data = {
            'count': 3000,
            'content': 'some new content'
        }
        return self.render_to_json_response(data)


class SerializedDetailView(JsonResponseMixin, View):
    def get(self, request, *args, **kwargs):
        obj = Update.objects.get(id=1)
        # data = {
        #     'user': obj.user.username,
        #     'content': obj.content
        # }
        json_data = obj.serialize()
        return HttpResponse(json_data, content_type='application/json')
        # return self.render_to_json_response(data)


class SerializedListView(JsonResponseMixin, View):
    def get(self, request, *args, **kwargs):
        # qs = Update.objects.all()
        # data = serialize('json', qs, fields=('user', 'content'))
        json_data = Update.objects.all().serialize()
        # json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')
        # return self.render_to_json_response(data)