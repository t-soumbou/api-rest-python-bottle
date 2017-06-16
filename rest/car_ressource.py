import persistence.car_persistence as commons_car_service
import commons.commons_utilitaire as commons_utilitaire
from bottle import get, post, put, delete, request, response, hook
from json import dumps
from entities.car import Car

car_service = commons_car_service.CarPersistence(Car)
invalid_parameters = "Invalid parameters"

@hook('after_request')
def init_response():
    response.content_type = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'

@get('/api/v1/car')
def get_all():
    response.status = 200
    cars = car_service.find_all()
    if cars is None:
        response.status = 404
    return dumps(cars, default=commons_utilitaire.jdefault)


@get('/api/v1/car/<car_id>')
def get_by_id(car_id):
    response.status = 200
    car = car_service.find_by_id(car_id)
    if car is None:
        response.status = 404
    return dumps(car, default= commons_utilitaire.jdefault)


@post('/api/v1/car')
def create_car():
    try:
        car = commons_utilitaire.get_record_from_body(request, Car)
        if car is None:
            return commons_utilitaire.error_handler(400, invalid_parameters, response)
        response.status = 201
        entity = commons_car_service.create(car)
        if entity is not None:
            return dumps(entity, default= commons_utilitaire.jdefault)
        else:
            return commons_utilitaire.error_handler(400, invalid_parameters, response)
    except TypeError:
        return commons_utilitaire.error_handler(400, invalid_parameters, response)


@put('/api/v1/car')
def update_car():
    try:
        response.status = 200
        car = commons_utilitaire.get_record_from_body(request, Car)
        result = commons_car_service.update(car)
    except TypeError:
        return commons_utilitaire.error_handler(400, invalid_parameters, response)
    if not result:
        return commons_utilitaire.error_handler(404, "identifiant not find", response)


@delete('/api/v1/car/<car_id>')
def delete_car(car_id):
    try:
        response.status = 200
        result = commons_car_service.delete_by_id(car_id)
    except TypeError:
        return commons_utilitaire.error_handler(400, invalid_parameters, response)
    if not result:
        return commons_utilitaire.error_handler(404, "identifiant not find", response)