#!/usr/bin/python3
"""Python file that works with api calls on city objects"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def state_city_without_id(state_id=None):
    """Handles http request for cities route with no id provided"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        objs = storage.all('City')
        obj_list = [obj.to_dict() for obj in objs.values()
                    if obj.state_id == state_id]
        return jsonify(obj_list)

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, "Not a Json")
        if data.get("name") is None:
            abort(400, "Missing name")
        data['state_id'] = state_id
        obj = City(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def state_city_with_id(city_id=None):
    """Handles http request for cities route with id"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404, "Not found")
    if request.method == 'GET':
        return jsonify(obj.to_dict())

    if request.method == 'DELETE':
        obj.delete()
        del obj
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400)
        IGNORE = ['id', 'created_at', 'updated_at', 'state_id']
        d = {k: v for k, v in data.items() if k not in IGNORE}
        for k, v in d.items():
            setattr(obj, k, v)
        obj.save()
        return jsonify(obj.to_dict()), 200
