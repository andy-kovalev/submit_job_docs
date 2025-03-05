from http import HTTPStatus

import pytest
from django.urls import reverse as url_reverse

from docs_metadata.urls import docs_metadata_url
from urls import url_path


@pytest.mark.django_db
def test_get_commands(not_authorized_ui_client, authorized_ui_client, command_factory):
    commands = command_factory(_quantity=6)

    url = '/' + url_path(docs_metadata_url, 'commands')

    response = not_authorized_ui_client.get(url)
    assert response.status_code == HTTPStatus.FOUND
    login_url = url_reverse('login')
    assert str(response.url).startswith(login_url)

    response = authorized_ui_client.get(url)
    assert response.status_code in (HTTPStatus.OK, HTTPStatus.FOUND)

    for command in commands:
        assert command.name in str(response.content)
