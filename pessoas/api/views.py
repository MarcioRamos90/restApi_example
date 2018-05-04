import json
from django.views.generic import View
from cfeapi.mixins import HttpResponseMixin

from .utils import is_json
from .mixins import CSRFExemptMixin

from pessoas.forms import PessoaForm
from pessoas.models import Pessoa


class PessoaListApiView(CSRFExemptMixin, HttpResponseMixin, View):
    is_json = True

    def get(self, request, *args, **kwargs):
        print(dir(request.parse_file_upload))
        print(request.scheme)
        # print(request.body.decode('utf-8') == '{}')

        if not request.body.decode('utf-8') == '{}':
            data = json.loads(request.body.decode('utf-8'))
            id_passad = data.get('id', None)
            if id_passad is not None:
                obj = Pessoa.objects.filter(id=id_passad)
                if obj.count() == 1:
                    json_data = obj.first().serialize()
                    return self.render_to_response(
                        data=json_data, status_code=200)
                data = json.dumps({'message': 'Object not found'})
                return self.render_to_response(data=data, status_code=404)
        obj = Pessoa.objects.all()
        json_data = obj.serialize()
        return self.render_to_response(data=json_data, status_code=200)
        data = json.dumps({'message': 'Not allowed, try later'})
        return self.render_to_response(data=data, status_code=500)

    def post(self, request, *args, **kwargs):
        valid_json = is_json(request.body.decode('utf-8'))

        if not valid_json:
            data = json.dumps({'message': 'Invalid json data'})
            return self.render_to_response(data=data, status_code=400)

        data = json.loads(request.body.decode('utf-8'))
        form = PessoaForm(data)
        if form.is_valid():
            obj = form.save(commit=True)
            data = obj.serialize()
            return self.render_to_response(data=data, status_code=200)
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data=data, status_code=400)

        data = json.dumps({'message': 'Not allowed, try later'})
        return self.render_to_response(data=data, status_code=500)

    def put(self, request, *args, **kwargs):
        valid_json = is_json(request.body.decode('utf-8'))

        if not valid_json:
            data = json.dumps({'message': 'Invalid json data'})
            return self.render_to_response(data=data, status_code=400)

        passed_data = json.loads(request.body.decode('utf-8'))
        data_id = passed_data.get('id', None)

        if data_id is None:
            data = json.dumps(
                {'id': 'This field is required to this opertion'})
            return self.render_to_response(data=data, status_code=404)
        # qs = Pessoa.objects.all()
        obj = Pessoa.objects.filter(id=data_id)
        if obj.first() is None:
            data = json.dumps({'message': 'Object not found'})
            return self.render_to_response(data=data, status_code=404)

        data = json.loads(obj.first().serialize())
        for key, item in passed_data.items():
            data[key] = item

        form = PessoaForm(data, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            data = json.dumps(data)
            return self.render_to_response(data=data, status_code=201)
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data=data, status_code=400)

        data = json.dumps({'message': 'Not allowed, try later'})
        return self.render_to_response(data=data, status_code=404)

    def delete(self, request, *args, **kwargs):
        valid_json = is_json(request.body.decode('utf-8'))

        if not valid_json:
            data = json.dumps({'message': 'Invalid json data'})
            return self.render_to_response(data=data, status_code=400)

        passed_data = json.loads(request.body.decode('utf-8'))
        data_id = passed_data.get('id', None)

        if data_id is None:
            data = json.dumps(
                {'id': 'This field is required to this opertion'})
            return self.render_to_response(data=data, status_code=404)

        obj = Pessoa.objects.filter(id=data_id)
        if obj.first() is None:
            data = json.dumps({'message': 'Object not found'})
            return self.render_to_response(data=data, status_code=404)

        message_status_delete, other = obj.delete()

        if message_status_delete == 1:
            data = json.dumps({'message': 'Successfully deleted.'})
            return self.render_to_response(data=data, status_code=200)

        data = json.dumps({'message': 'Not allowed, try later'})
        return self.render_to_response(data=data, status_code=404)