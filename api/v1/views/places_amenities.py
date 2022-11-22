#!/usr/bin/python3
"""Python file that works with api calls on Place and Amenity objects"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import environ


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def place_amenities(place_id=None):
    """Handles http requst without id for amenities linked with places"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    objs = storage.all('Amenity')
    if environ.get('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amen_ids = place.amenities
        place_amenities = []
        for id in place_amen_ids:
            place_amenities.append(storage.get(Amenity, id))
    place_amenities = [
        obj.to_dict() for obj in place_amenities
        ]
    return jsonify(place_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'])
def amenity_to_place(place_id=None, amenity_id=None):
    """Handles http requests with id for amenties linked with places"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)

    if request.method == 'DELETE':
        if (amenity not in place.amenities and
                amenity.id not in place.amenities):
            abort(404)
        if environ.get('HBNB_TYPE_STORAGE') == 'db':
            place.amenities.remove(amenity)
        else:
            place.amenity_ids.pop(amenity.id, None)
        place.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if (amenity in place.amenities or
                amenity.id in place.amenities):
            return jsonify(amenity.to_dict()), 200
        if environ.get('HBNB_TYPE_STORAGE') == 'db':
            place.amenities.append(amenity)
        else:
            place.amenities = amenity
        place.save()
        return jsonify(amenity.to_dict()), 201
