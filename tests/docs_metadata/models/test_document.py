import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError, DataError

from tests import get_random_string
from tests.docs_metadata.models import SQLITE_DB_ENGINE
from docs_metadata.models import Document, ParseMode


@pytest.mark.django_db
def test_get_documents(document_factory):
    documents = document_factory(_quantity=4)

    documents_from_db = Document.objects.all()
    assert len(documents) == len(documents_from_db)


@pytest.mark.django_db
def test_get_document(document_factory):
    documents = document_factory(_quantity=2)

    document = Document.objects.get(id=documents[0].id)
    assert document.text == documents[0].text


@pytest.mark.django_db
def test_create_document(command_factory):
    document_text = 'test_create_document'
    document = Document.objects.create(order_index=1,
                                       file_prefix=get_random_string(10),
                                       index_text=get_random_string(5),
                                       text=document_text,
                                       parse_mode=ParseMode.MARKDOWN,
                                       remove_buttons_before_message=False)
    document.buttons.set(command_factory(_quantity=2))

    document = Document.objects.get(id=document.id)
    assert document.text == document_text


@pytest.mark.parametrize(['attribute', 'default_value'],
                         (('parse_mode', ParseMode.MARKDOWN),
                          ('remove_buttons_before_message', False),))
@pytest.mark.django_db
def test_constraints_default_create_document(command_factory, attribute, default_value):
    document = Document.objects.create(order_index=1,
                                       file_prefix=get_random_string(10),
                                       index_text=get_random_string(5),
                                       text=get_random_string(10),
                                       remove_buttons_before_message=False)
    document.buttons.set(command_factory(_quantity=2))

    document = Document.objects.get(id=document.id)
    assert document.__getattribute__(attribute) == default_value


@pytest.mark.parametrize('attribute',
                         ('order_index',
                          'file_prefix',))
@pytest.mark.django_db
def test_constraints_not_null_create_document(command_factory, attribute):
    err_not_null_constraint = ('not', 'null', 'constraint')

    remove_buttons_before_message_param = None if attribute == 'remove_buttons_before_message' else False
    with pytest.raises(IntegrityError) as exc_info:
        Document.objects.create(order_index=None if attribute == 'order_index' else 1,
                                file_prefix=None if attribute == 'file_prefix' else get_random_string(10),
                                index_text=None if attribute == 'index_text' else get_random_string(5),
                                remove_buttons_before_message=remove_buttons_before_message_param)
    err_text = str(exc_info.value).lower()
    assert err_text.__contains__(err_not_null_constraint[0]) and err_text.__contains__(
        err_not_null_constraint[1]) and err_text.__contains__(err_not_null_constraint[2])


@pytest.mark.parametrize(['attribute', 'max_length'],
                         (('file_prefix', 256),
                          ('index_text', 5),))
@pytest.mark.django_db
def test_constraints_max_length_create_document(command_factory, attribute, max_length):
    if settings.DATABASES['default']['ENGINE'] == SQLITE_DB_ENGINE:
        exception_class = ValidationError
    else:
        exception_class = DataError
    with pytest.raises(exception_class) as exc_info:
        company = Document.objects.create(
            order_index=1,
            file_prefix=get_random_string(max_length + 1) if attribute == 'file_prefix' else get_random_string(10),
            index_text=get_random_string(max_length + 1) if attribute == 'index_text' else get_random_string(5),
            text=get_random_string(max_length + 1) if attribute == 'text' else get_random_string(10),
            remove_buttons_before_message=False)
        company.full_clean()
    assert str(max_length) in str(exc_info.value)


@pytest.mark.django_db
def test_update_document(document_factory):
    document_text = 'test_create_document'
    document = document_factory(_quantity=1)[0]

    document = Document.objects.get(id=document.id)
    assert document.text != document_text

    document.text = document_text
    document.save()

    document = Document.objects.get(id=document.id)
    assert document.text == document_text


@pytest.mark.django_db
def test_delete_document(document_factory):
    document_factory(_quantity=1)

    documents = Document.objects.all()
    assert len(documents) == 1

    documents[0].delete()

    documents = Document.objects.all()
    assert len(documents) == 0
