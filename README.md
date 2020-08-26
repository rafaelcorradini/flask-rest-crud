# flask-rest-crud

Python package that generate REST API CRUD from mongoengine models.

The generated API can be used with [react-admin](https://marmelab.com/react-admin/DataProviders.html) since it has the [Simple REST Data Provider](https://marmelab.com/react-admin/DataProviders.html) dialect.

## Install

```shell
pip install flask-rest-crud
```

## Usage

```python
from flask_rest_crud import Crud, init_crud_error_handler
from flask_mongoengine import MongoEngine

db = MongoEngine()

class Category(db.Document):
    name = db.StringField(required=True)
    description = db.StringField()

Crud(app, Category, 'categories')

errors = Blueprint('errors', __name__)
init_crud_error_handler(errors, app)
```

## Example

```python
from flask import Flask
from project.crud import Crud
from project.models.category import Category
from flask_mongoengine import MongoEngine
from flask_rest_crud import Crud, init_crud_error_handler

db = MongoEngine()


# models
class Category(db.Document):
    name = db.StringField(required=True)
    description = db.StringField()

class Product(db.Document):
    name = db.StringField(required=True)
    description = db.StringField()
    category = db.ReferenceField(Category)


# Create application
app = Flask(__name__)

# CRUDS
Crud(app, Category, 'categories', '/api/')
Crud(app, Product, 'products', '/api/')


# Error handler

errors = Blueprint('errors', __name__)
init_crud_error_handler(errors, app)


#  mongodb config
app.config['SECRET_KEY'] = '123456790'
app.config['MONGODB_SETTINGS'] = { 'host': 'hosturi' }

# Create models

db.init_app(app)
app = create_app()
app.run()
```

This code will generate the following API endpoints:

| Method             | API calls                                                                                  |
| ------------------ | ---------------------------------------------------------------------------------------    |
| `getList`          | `GET http://my.api.url/api/products?sort=["name","ASC"]&range=[0, 24]&filter={"name":"bar"}`   |
| `getOne`           | `GET http://my.api.url/api/products/123`                                                       |
| `getMany`          | `GET http://my.api.url/api/products?filter={"id":[123,456,789]}`                               |
| `getManyReference` | `GET http://my.api.url/api/products?filter={"category_id":345}`                                |
| `create`           | `POST http://my.api.url/api/products`                                                          |
| `update`           | `PUT http://my.api.url/api/products/123`                                                       |
| `delete`           | `DELETE http://my.api.url/api/products/123`                                                    |




