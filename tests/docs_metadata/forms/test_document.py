import pytest

from docs_metadata.forms import DocumentForm
from docs_metadata.models import ParseMode
from tests import get_random_string


@pytest.mark.django_db
def test_get_document(command_factory):
    data = {'order_index': 1,
            'file_prefix': get_random_string(10),
            'index_text': get_random_string(5),
            'text': get_random_string(10),
            'parse_mode': ParseMode.MARKDOWN.name,
            'remove_buttons_before_message': False
            }

    form = DocumentForm(data=data)
    assert form.is_valid()
