from http import HTTPStatus

from docs_metadata.urls import docs_metadata_url
from urls import api_url_path


def test_get_parse_modes(not_authorized_api_client, authorized_api_client):
    url = '/' + api_url_path(docs_metadata_url, 'parsemodes')

    response = not_authorized_api_client.get(url)
    assert response.status_code == HTTPStatus.FORBIDDEN

    response = authorized_api_client.get(url)
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert len(data) == 1
    assert 'ParseMode' in data.keys()

    assert len(data['ParseMode']) == 3
    assert data['ParseMode'][0] == 'MARKDOWN'
    assert data['ParseMode'][1] == 'MARKDOWN_V2'
    assert data['ParseMode'][2] == 'HTML'
