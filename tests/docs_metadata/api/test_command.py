from http import HTTPStatus

import pytest

from docs_metadata.models import Command
from docs_metadata.urls import docs_metadata_url
from tests import get_random_string
from submit_job_docs.urls import api_url_path


@pytest.mark.django_db
def test_get_commands(not_authorized_api_client, authorized_api_client, command_factory):
    commands = command_factory(_quantity=6)

    url = '/' + api_url_path(docs_metadata_url, 'commands')

    response = not_authorized_api_client.get(url)
    assert response.status_code == HTTPStatus.FORBIDDEN

    response = authorized_api_client.get(url)
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert len(data['results']) == len(commands)


@pytest.mark.django_db
def test_get_command(not_authorized_api_client, authorized_api_client, command_factory):
    commands = command_factory(_quantity=2)

    url = '/' + api_url_path(docs_metadata_url, 'commands', f'{commands[0].id}')

    response = not_authorized_api_client.get(url)
    assert response.status_code == HTTPStatus.FORBIDDEN

    response = authorized_api_client.get(url)
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data['name'] == commands[0].name


@pytest.mark.django_db
def test_create_command(not_authorized_api_client, authorized_api_client):
    command_name = 'test_create_command'
    data = {"action": "ADD",
            "name": command_name,
            "title": get_random_string(10),
            "prefix": get_random_string(10)
            }

    url = '/' + api_url_path(docs_metadata_url, 'commands')

    response = not_authorized_api_client.post(url, data=data)
    assert response.status_code == HTTPStatus.FORBIDDEN

    response = authorized_api_client.post(url, data=data)
    assert response.status_code == HTTPStatus.CREATED

    commands = Command.objects.all()
    assert len(commands) == 1
    assert commands[0].name == command_name


@pytest.mark.django_db
def test_update_command(not_authorized_api_client, authorized_api_client, command_factory):
    command = command_factory(_quantity=1)[0]

    command_name = 'test_create_command'
    data = {'name': command_name}

    url = '/' + api_url_path(docs_metadata_url, 'commands', f'{command.id}')

    response = not_authorized_api_client.patch(url, data=data)
    assert response.status_code == HTTPStatus.FORBIDDEN

    response = authorized_api_client.patch(url, data=data)
    assert response.status_code == HTTPStatus.OK

    commands = Command.objects.all()
    assert commands[0].name == command_name


@pytest.mark.django_db
def test_delete_command(not_authorized_api_client, authorized_api_client, command_factory):
    command = command_factory(_quantity=1)[0]

    url = '/' + api_url_path(docs_metadata_url, 'commands', f'{command.id}')

    response = not_authorized_api_client.delete(url)
    assert response.status_code == HTTPStatus.FORBIDDEN

    response = authorized_api_client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT

    commands = Command.objects.all()
    assert len(commands) == 0
