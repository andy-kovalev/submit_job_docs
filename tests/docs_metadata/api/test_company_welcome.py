from http import HTTPStatus

import pytest

from docs_metadata.models import CompanyWelcome
from docs_metadata.urls import docs_metadata_url
from tests import get_random_string
from submit_job_docs.urls import api_url_path


@pytest.mark.django_db
def test_get_company(not_authorized_api_client, authorized_api_client, company_welcome_factory):
    url = '/' + api_url_path(docs_metadata_url, 'company', 'welcome')

    response = not_authorized_api_client.get(url)
    assert response.status_code == HTTPStatus.FORBIDDEN

    response = authorized_api_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND

    company = company_welcome_factory(_quantity=1)[0]

    response = authorized_api_client.get(url)
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data['help_text'] == company.help_text


@pytest.mark.django_db
def test_create_company(not_authorized_api_client, authorized_api_client, company_welcome_factory, command_factory):
    url = '/' + api_url_path(docs_metadata_url, 'company', 'welcome')

    company_start_text = 'test_create_company_start_text'
    commands = command_factory(_quantity=5)

    data = {"help_command": commands[0].id,
            "add_document_command": commands[1].id,
            "add_next_document_command": commands[2].id,
            "end_document_command": commands[3].id,
            "cancel_command": commands[4].id,
            "readd_document_text": get_random_string(10),
            "help_text": get_random_string(10),
            "start_text": company_start_text}

    response = not_authorized_api_client.post(url, data=data)
    assert response.status_code == HTTPStatus.FORBIDDEN

    response = authorized_api_client.post(url, data=data)
    assert response.status_code == HTTPStatus.CREATED

    company = CompanyWelcome.objects.all()
    assert len(company) == 1
    assert company[0].start_text == company_start_text


@pytest.mark.django_db
def test_update_company(not_authorized_api_client, authorized_api_client, company_welcome_factory):
    company_welcome_factory(_quantity=1)

    company_start_text = 'test_create_company_start_text'
    data = {'start_text': company_start_text}

    url = '/' + api_url_path(docs_metadata_url, 'company', 'welcome')

    response = not_authorized_api_client.patch(url, data=data)
    assert response.status_code == HTTPStatus.FORBIDDEN

    response = authorized_api_client.patch(url, data=data)
    assert response.status_code == HTTPStatus.OK

    company = CompanyWelcome.objects.all()
    assert company[0].start_text == company_start_text


@pytest.mark.django_db
def test_delete_company(not_authorized_api_client, authorized_api_client, company_welcome_factory):
    company = company_welcome_factory(_quantity=1)[0]

    url = '/' + api_url_path(docs_metadata_url, 'company', 'welcome', '{id}')

    response = authorized_api_client.delete(
        '/' + api_url_path(docs_metadata_url, 'commands', f'{company.add_document_command.id}'))
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

    response = not_authorized_api_client.delete(url.format(id=company.id))
    assert response.status_code == HTTPStatus.FORBIDDEN

    response = authorized_api_client.delete(url.format(id=company.id))
    assert response.status_code == HTTPStatus.NO_CONTENT

    company = CompanyWelcome.objects.all()
    assert len(company) == 0
