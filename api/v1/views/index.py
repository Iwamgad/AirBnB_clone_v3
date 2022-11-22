#!/usr/bin/python3
"""Python file that routes the Flask API's"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage

from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State


@app_views.route('/status', methods=['GET'])
def show_status():
    """An end point to retrive ok status as a response"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """An endpoint to retrive the number of each objects by type"""
    mapper = {
            "amenities": Amenity,
            "cities": City,
            "places": Place,
            "reviews": Review,
            "states": State,
            "users": User
            }

    result = {}
    for k, v in mapper.items():
        result[k] = storage.count(v)

    return jsonify(result)
