import pytest

from docs_metadata.forms import CompanyWelcomeForm
from docs_metadata.models import Action
from tests import get_random_string


@pytest.mark.django_db
def test_get_company(command_factory):
    help_command = command_factory(_quantity=1, action=Action.HELP)[0]
    add_document_command = command_factory(_quantity=1, action=Action.ADD)[0]
    add_next_document_command = command_factory(_quantity=1, action=Action.ADD_NEXT)[0]
    end_document_command = command_factory(_quantity=1, action=Action.END)[0]
    cancel_command = command_factory(_quantity=1, action=Action.CANCEL)[0]

    data = {'help_command': help_command.pk,
            'add_document_command': add_document_command.pk,
            'add_next_document_command': add_next_document_command.pk,
            'end_document_command': end_document_command.pk,
            'cancel_command': cancel_command.pk,
            'readd_document_text': get_random_string(10),
            'help_text': get_random_string(10),
            'start_text': get_random_string(10)
            }

    form = CompanyWelcomeForm(data=data)
    assert form.is_valid()
