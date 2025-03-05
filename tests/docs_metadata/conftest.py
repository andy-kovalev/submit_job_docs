import random
import string

import pytest
# noinspection PyPackageRequirements
from model_bakery import baker

from docs_metadata.models import Command, CompanyWelcome, Document


@pytest.fixture
def command_factory():
    def factory(*args, **kwargs):
        return baker.make(Command, *args, **kwargs)

    return factory


@pytest.fixture
def company_welcome_factory():
    def factory(*args, **kwargs):
        return baker.make(CompanyWelcome, *args, **kwargs)

    return factory


@pytest.fixture
def document_factory():
    def factory(*args, **kwargs):
        return baker.make(Document, *args, **kwargs)

    return factory


@pytest.fixture
def commands_fixture(command_factory):
    def get_random_prefix(length):
        return ''.join(random.choice(string.printable) for i in range(length))

    commands = command_factory(_quantity=2)
    commands += command_factory(_quantity=1, prefix=get_random_prefix(20))
    commands += command_factory(_quantity=1, prefix=get_random_prefix(25))
    return commands
