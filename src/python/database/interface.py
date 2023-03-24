import json
import requests
from requests import Request, Session

from src.python.param import http
from src.python.database import digikala


DIGIKALA = "digikala"

sources = [
    DIGIKALA,
]


def fetch_data(source):
    url = "http://httpbin.org/anything"
    data = None
    if source == DIGIKALA:
        data = digikala.get_data()

    return data



