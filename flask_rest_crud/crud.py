from flask import request, Response
import json
from mongoengine import ReferenceField


class Crud:
    def __init__(self, app, model, name, prefix='/'):
        self.app = app
        self.model = model
        self.name = name
        self.prefix = prefix
        self.create_routes()

    def create_routes(self):
        self.app.add_url_rule(f'{self.prefix}/{self.name}', f'${self.name}_list', self.list, methods=['GET'])
        self.app.add_url_rule(f'{self.prefix}/{self.name}', f'${self.name}_create', self.create, methods=['POST'])
        self.app.add_url_rule(f'{self.prefix}/{self.name}/<model_id>', f'${self.name}_update', self.update, methods=['PUT'])
        self.app.add_url_rule(f'{self.prefix}/{self.name}/<model_id>', f'${self.name}_delete', self.delete, methods=['DELETE'])

    def create(self):
        data = request.get_json()
        model = self.model()
        normalized_data = {}
        for k, v in data.items():
            if '_id' in k:
                normalized_data[k.replace('_id', '')] = v
            else:
                normalized_data[k] = v

        for field, cls in self.model._fields.items():
            if field in normalized_data:
                if isinstance(cls, ReferenceField):
                    model[field] = self.model.category.document_type_obj.objects.get(id=normalized_data[field])
                else:
                    model[field] = normalized_data[field]
        model.save()
        return model.to_json()

    def update(self, model_id):
        data = request.get_json()
        model = self.model.objects.get(id=model_id)
        for field in self.model._fields:
            if field in data:
                model[field] = data[field]
        model.save()
        return model.to_json()

    def find(self, model_id):
        model = self.model.objects.get(id=model_id)
        return model.to_json()

    def delete(self, model_id):
        model = self.model.objects.get(id=model_id)
        model.delete()
        return model.to_json()

    def list(self):
        count = self.model.objects.count()
        start = 0
        end = count
        if request.args.get('range'):
            pagination = json.loads(request.args.get('range'))
            start = pagination[0]
            end = pagination[1]

        if request.args.get('filter'):
            filters = json.loads(request.args.get('filter'))
            normalized_filters = {}
            for key, value in filters.items():
                if type(value) is list:
                    normalized_filters[f'{key}__in'] = value
                else:
                    normalized_filters[f'{key}'] = value
            items = self.model.objects(**normalized_filters)
        else:
            items = self.model.objects

        if request.args.get('sort'):
            sort = json.loads(request.args.get('sort'))
            direction = '-' if sort[1] == 'DESC' else ''
            items = items.skip(start).limit(end - start).order_by(f'{direction}{sort[0]}')
        else:
            items = items.skip(start).limit(end - start)

        res = Response(items.to_json())
        res.headers['Content-Range'] = f'{self.name} {start}-{end}/{count}'
        return res
