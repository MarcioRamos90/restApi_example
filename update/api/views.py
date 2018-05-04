import json
from django.views.generic import View

from cfeapi.mixins import HttpResponseMixin

from update.forms import UpdateModelForm
from update.models import Update as UpdateModel

from .mixins import CSRFExemptMixin
from .utils import is_json

class UpdateModelDatailAPIView(HttpResponseMixin, CSRFExemptMixin, View):
    is_json = True

    def get_object(self, id=None):
        # try:
        #     UpdateModel.objects.get(id=id)
        # except UpdateModel.DoesNotExist:
        #         obj = None
        # return obj
        """
        Below handles a Does Not Exist Exception too
        """
        qs = UpdateModel.objects.filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def get(self, request, id, *args, **kwargs):
        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({"message": "Update not found"})
            return self.render_to_response(data=error_data, status_code=404)
        json_data = obj.serialize()
        return self.render_to_response(data=json_data)

    def post(self, request, id, *args, **kwargs):
        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({"message": "Update not found"})
            return self.render_to_response(data=error_data, status_code=404)
        data = json.dumps(
            {"message": "Not allowed plese use api/updates endpoint"})
        return self.render_to_response(data=data, status_code=403)

    def put(self, request, id, *args, **kwargs):
        valid_json = is_json(request.body.decode('utf-8'))
        if not valid_json:
            error_data = json.dumps(
                {"message": "Invalid data sent, please send using JSON"})
            return self.render_to_response(data=error_data, status_code=400)

        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({"message": "Update not found"})
            return self.render_to_response(data=error_data, status_code=404)
        print(request.body)

        data = json.loads(obj.serialize())
        passed_data = json.loads(request.body.decode('utf-8'))

        for key, value in passed_data.items():
            data[key] = value
        form = UpdateModelForm(data, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = json.dumps(data)
            return self.render_to_response(obj_data, status_code=201)
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data=data, status_code=400)

        # new_data = json.loads(request.body.decode('utf-8'))
        # print(new_data['content'])
        data = json.dumps({"message": "alterado com successo"})
        return self.render_to_response(data=data)

    def delete(self, request, id, *args, **kwargs):
        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({"message": "Update not found"})
            return self.render_to_response(data=error_data, status_code=404)
        deleted_, item_delete = obj.delete()
        print(deleted_)
        if deleted_ == 1:
            data = json.dumps({"message": "Successfully deleted."})
            return self.render_to_response(data=data, status_code=200)
        data = json.dumps(
            {"message": "Could not delete item. Please try again later"})
        return self.render_to_response(data=data, status_code=400)


class UpdateModelListAPIView(HttpResponseMixin, CSRFExemptMixin, View):
    is_json = True
    queryset = None

    def get_queryset(self):
        qs = UpdateModel.objects.all()
        self.queryset = qs
        return self.queryset

    def get_object(self, id=None):
        if id is None:
            return None
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def get(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        passad_id = data.get('id', None)
        print('id', passad_id)
        if passad_id is not None:
            obj = self.get_object(id=passad_id)
            if obj is None:
                error_data = json.dumps(
                    {"message": "Not found 1"})
                return self.render_to_response(
                    data=error_data, status_code=404)
            json_data = obj.serialize()
            return self.render_to_response(data=json_data)
        else:
            qs = self.get_queryset()
            json_data = qs.serialize()
            return self.render_to_response(data=json_data)

    def post(self, request, *args, **kwargs):

        valid_json = is_json(request.body.decode('utf-8'))
        if not valid_json:
            error_data = json.dumps(
                {"message": "Invalid data sent, please send using JSON"})
            return self.render_to_response(data=error_data, status_code=400)

        data = json.loads(request.body.decode('utf-8'))
        form = UpdateModelForm(data)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = obj.serialize()
            return self.render_to_response(obj_data, status_code=201)
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data=data, status_code=400)
        data = {"message": 'Not allowad for now!'}
        return self.render_to_response(data=data, status_code=500)

    def put(self, request, *args, **kwargs):
        valid_json = is_json(request.body.decode('utf-8'))
        if not valid_json:
            error_data = json.dumps(
                {"message": "Invalid data sent, please send using JSON"})
            return self.render_to_response(data=error_data, status_code=400)

        passed_data = json.loads(request.body.decode('utf-8'))
        passad_id = passed_data.get('id', None)
        if passad_id is None:
            error_data = json.dumps(
                {"id": "this field is riquired"})
            return self.render_to_response(data=error_data, status_code=400)

        obj = self.get_object(id=passad_id)
        if obj is None:
            error_data = json.dumps({"message": "Object not found"})
            return self.render_to_response(data=error_data, status_code=404)
        print(request.body)

        data = json.loads(obj.serialize())

        for key, value in passed_data.items():
            data[key] = value
        form = UpdateModelForm(data, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = json.dumps(data)
            return self.render_to_response(obj_data, status_code=201)
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data=data, status_code=400)

        # new_data = json.loads(request.body.decode('utf-8'))
        # print(new_data['content'])
        data = json.dumps({"message": "alterado com successo"})
        return self.render_to_response(data=data)

    def delete(self, request, *args, **kwargs):
        valid_json = is_json(request.body.decode('utf-8'))
        if not valid_json:
            error_data = json.dumps(
                {"message": "Invalid data sent, please send using JSON"})
            return self.render_to_response(data=error_data, status_code=400)

        passed_data = json.loads(request.body.decode('utf-8'))
        passad_id = passed_data.get('id', None)
        if passad_id is None:
            error_data = json.dumps(
                {"id": "this field is riquired"})
            return self.render_to_response(data=error_data, status_code=400)

        obj = self.get_object(id=passad_id)
        if obj is None:
            error_data = json.dumps({"message": "Object not found"})
            return self.render_to_response(data=error_data, status_code=404)

        deleted_, item_delete = obj.delete()
        print(deleted_)
        if deleted_ == 1:
            data = json.dumps({"message": "Successfully deleted."})
            return self.render_to_response(data=data, status_code=200)
        data = json.dumps(
            {"message": "Could not delete item. Please try again later"})
        return self.render_to_response(data=data, status_code=400)


    # def delete(self, request, *args, **kwargs):

    #     data = json.dumps(
    #         {"message": "you can't dalete a list"})
    #     return self.render_to_response(data=data, status_code=403)
