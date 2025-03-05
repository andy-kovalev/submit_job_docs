import pytest

from docs_metadata.forms import CommandForm
from tests import get_random_string


@pytest.mark.django_db
def test_get_command():
    data = {'action': 'ADD_NEXT',
            'name': get_random_string(10),
            'title': get_random_string(10),
            'prefix': get_random_string(10)
            }

    form = CommandForm(data=data)
    assert form.is_valid()
