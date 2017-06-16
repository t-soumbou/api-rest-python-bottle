from rest.car_ressource import *
from rest.driver_ressource  import *


@get('/api/v1/check')
def check():
    return "ok"


def run(host, port):
    from bottle import run
    run(host=host, port=port)