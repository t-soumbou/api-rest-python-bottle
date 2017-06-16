import persistence.driver_persistence as commons_driver_service
import commons.commons_utilitaire as commons_utilitaire
from bottle import get, post, put, delete, request, response, hook
from json import dumps
from entities.driver import Driver

driver_service = commons_driver_service.DriverPersistence(Driver)
invalid_parameters = "Invalid parameters"

@hook('after_request')
def init_response():
    response.content_type = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'


@get('/api/v1/driver')
def get_all():
    response.status = 200
    drivers = driver_service.find_all()
    if drivers is None:
        response.status = 404
    return dumps(drivers, default=commons_utilitaire.jdefault)


@get('/api/v1/driver/<driver_id>')
def get_by_id(driver_id):
    response.status = 200
    driver = driver_service.find_by_id(driver_id)
    if driver is None:
        response.status = 404
    return dumps(driver, default=commons_utilitaire.jdefault)


@post('/api/v1/driver')
def create_driver():
    try:
        driver = commons_utilitaire.get_record_from_body(request, Driver)
        response.status = 201
        return dumps(commons_driver_service.create(driver), default=commons_utilitaire.jdefault)
    except TypeError:
        return commons_utilitaire.error_handler(400, invalid_parameters, response)


@put('/api/v1/driver')
def update_driver():
    try:
        response.status = 200
        driver = commons_utilitaire.get_record_from_body(request, Driver)
        result = commons_driver_service.update(driver)
    except TypeError:
        return commons_utilitaire.error_handler(400, invalid_parameters, response)
    if not result:
        return commons_utilitaire.error_handler(404, "identifiant not find", response)


@delete('/api/v1/driver/<driver_id>')
def delete_driver(driver_id):
    try:
        response.status = 200
        result = commons_driver_service.delete_by_id(driver_id)
    except TypeError:
        return commons_utilitaire.error_handler(400, invalid_parameters, response)
    if not result:
        return commons_utilitaire.error_handler(404, "identifiant not find", response)

