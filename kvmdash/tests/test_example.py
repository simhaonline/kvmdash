from flask import Flask
from kvmdash import kvmdash
import pytest

def test_app():
    #kvmdash = Flask(__name__)
    #from kvmdash import views
    kvmdash.testing = True

    # app.run() # this actually works here...
    with kvmdash.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.data == "Hello World!"
        print response.headers
        assert False
