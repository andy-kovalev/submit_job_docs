from http import HTTPStatus

from docs_metadata.urls import docs_metadata_url
from submit_job_docs.urls import api_url_path


def test_get_actions(not_authorized_api_client, authorized_api_client):
    url = '/' + api_url_path(docs_metadata_url, 'actions')

    response = not_authorized_api_client.get(url)
    assert response.status_code == HTTPStatus.FORBIDDEN

    response = authorized_api_client.get(url)
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert len(data) == 1
    assert 'Action' in data.keys()

    assert len(data['Action']) == 5
    assert data['Action'][0] == 'ADD'
    assert data['Action'][1] == 'ADD_NEXT'
    assert data['Action'][2] == 'END'
    assert data['Action'][3] == 'CANCEL'
    assert data['Action'][4] == 'HELP'
