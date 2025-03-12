import pytest
from django.test import RequestFactory
from django.urls import Resolver404

from submit_job_docs.asgi import application as asgi
from submit_job_docs.wsgi import application as wsgi


def test_asgi_request(rf: RequestFactory):
    with pytest.raises(Resolver404):
        asgi.resolve_request(rf.get("/"))


def test_wsgi_request(rf: RequestFactory):
    with pytest.raises(Resolver404):
        wsgi.resolve_request(rf.get("/"))
