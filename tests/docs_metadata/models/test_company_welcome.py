import pytest
from django.core.exceptions import ValidationError

from tests import get_random_string
from docs_metadata.models import CompanyWelcome


@pytest.mark.django_db
def test_get_company(company_welcome_factory):
    company = company_welcome_factory(_quantity=1)[0]

    company_from_db = CompanyWelcome.objects.get(id=company.id)
    assert company_from_db.start_text == company.start_text


@pytest.mark.django_db
def test_create_company(command_factory):
    company_start_text = 'test_create_company'
    commands = command_factory(_quantity=5)

    company = CompanyWelcome.objects.create(help_command=commands[0],
                                            add_document_command=commands[1],
                                            add_next_document_command=commands[2],
                                            end_document_command=commands[3],
                                            cancel_command=commands[4],
                                            readd_document_text=get_random_string(10),
                                            help_text=get_random_string(10),
                                            start_text=company_start_text)

    company = CompanyWelcome.objects.get(id=company.id)
    assert company.start_text == company_start_text

    with pytest.raises(ValidationError) as exc_info:
        CompanyWelcome.objects.create(help_command=commands[0],
                                      add_document_command=commands[1],
                                      add_next_document_command=commands[2],
                                      end_document_command=commands[3],
                                      cancel_command=commands[4],
                                      readd_document_text=get_random_string(10),
                                      help_text=get_random_string(10),
                                      start_text=get_random_string(10))
    assert 'Company Welcome already exists' in str(exc_info.value)


@pytest.mark.parametrize(['attribute', 'max_length'],
                         (('readd_document_text', 256),))
@pytest.mark.django_db
def test_constraints_max_length_create_company(command_factory, attribute, max_length):
    commands = command_factory(_quantity=5)

    with pytest.raises(ValidationError) as exc_info:
        company = CompanyWelcome(
            help_command=commands[0],
            add_document_command=commands[1],
            add_next_document_command=commands[2],
            end_document_command=commands[3],
            cancel_command=commands[4],
            readd_document_text=get_random_string(
                max_length + 1) if attribute == 'readd_document_text' else get_random_string(10),
            help_text=get_random_string(max_length + 1) if attribute == 'help_text' else get_random_string(10),
            start_text=get_random_string(max_length + 1) if attribute == 'start_text' else get_random_string(10))
        company.full_clean()
    assert str(max_length) in str(exc_info.value)


@pytest.mark.django_db
def test_update_company(company_welcome_factory):
    company_start_text = 'test_create_company'
    company = company_welcome_factory(_quantity=1)[0]

    company = CompanyWelcome.objects.get(id=company.id)
    assert company.start_text != company_start_text

    company.start_text = company_start_text
    company.save()

    company = CompanyWelcome.objects.get(id=company.id)
    assert company.start_text == company_start_text


@pytest.mark.django_db
def test_delete_company(company_welcome_factory):
    company_welcome_factory(_quantity=1)

    company = CompanyWelcome.objects.all()
    assert len(company) == 1

    company[0].delete()

    company = CompanyWelcome.objects.all()
    assert len(company) == 0
