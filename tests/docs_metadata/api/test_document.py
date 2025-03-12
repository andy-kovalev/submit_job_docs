from http import HTTPStatus

import pytest

from docs_metadata.models import Document
from docs_metadata.models import ParseMode
from docs_metadata.urls import docs_metadata_url
from tests import get_random_string
from submit_job_docs.urls import api_url_path


@pytest.mark.django_db
def test_get_documents(not_authorized_api_client, authorized_api_client, document_factory):
    documents = document_factory(_quantity=4)
    documents.sort(key=lambda d: d.order_index)

    url = '/' + api_url_path(docs_metadata_url, 'documents')

    response = not_authorized_api_client.get(url)
    assert response.status_code == HTTPStatus.FORBIDDEN

    response = authorized_api_client.get(url)
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert len(data) == len(documents)

    for i, c in enumerate(data['results']):
        assert c['file_prefix'] == documents[i].file_prefix


@pytest.mark.django_db
def test_get_document(not_authorized_api_client, authorized_api_client, document_factory):
    documents = document_factory(_quantity=2)

    url = '/' + api_url_path(docs_metadata_url, 'documents', f'{documents[0].id}')

    response = not_authorized_api_client.get(url)
    assert response.status_code == HTTPStatus.FORBIDDEN

    response = authorized_api_client.get(url)
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data['file_prefix'] == documents[0].file_prefix


@pytest.mark.django_db
def test_create_document(not_authorized_api_client, authorized_api_client, command_factory):
    commands = command_factory(_quantity=2)

    document_index_text = 'test'
    data = {"order_index": "1",
            "file_prefix": get_random_string(10),
            "index_text": document_index_text,
            "end_document_command": commands[0].id,
            "text": get_random_string(10),
            "buttons": [commands[0].id, commands[1].id],
            "parse_mode": ParseMode.MARKDOWN.name,
            "remove_buttons_before_message": "False"}

    url = '/' + api_url_path(docs_metadata_url, 'documents')

    response = not_authorized_api_client.post(url, data=data)
    assert response.status_code == HTTPStatus.FORBIDDEN

    response = authorized_api_client.post(url, data=data)
    assert response.status_code == HTTPStatus.CREATED

    documents = Document.objects.all()
    assert len(documents) == 1
    assert documents[0].index_text == document_index_text


@pytest.mark.django_db
def test_update_document(not_authorized_api_client, authorized_api_client, document_factory):
    document = document_factory(_quantity=1)[0]

    document_index_text = 'test'
    data = {'index_text': document_index_text}

    url = '/' + api_url_path(docs_metadata_url, 'documents', f'{document.id}')

    response = not_authorized_api_client.patch(url, data=data)
    assert response.status_code == HTTPStatus.FORBIDDEN

    response = authorized_api_client.patch(url, data=data)
    assert response.status_code == HTTPStatus.OK

    documents = Document.objects.all()
    assert documents[0].index_text == document_index_text


@pytest.mark.django_db
def test_delete_document(not_authorized_api_client, authorized_api_client, document_factory):
    document = document_factory(_quantity=1)[0]

    url = '/' + api_url_path(docs_metadata_url, 'documents', f'{document.id}')

    response = not_authorized_api_client.delete(url)
    assert response.status_code == HTTPStatus.FORBIDDEN

    response = authorized_api_client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT

    documents = Document.objects.all()
    assert len(documents) == 0
