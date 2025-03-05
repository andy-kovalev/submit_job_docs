import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from tests import get_random_string
from docs_metadata.models import Command, Action


@pytest.mark.django_db
def test_get_commands(commands_fixture):
    commands = commands_fixture

    commands_from_db = Command.objects.all()
    assert len(commands) == len(commands_from_db)

    for i, command in enumerate(commands_from_db):
        if commands_from_db[i].prefix:
            assert f"{command.title} ({command.name}:{command.prefix})" == str(commands_from_db[i])
        else:
            assert f"{command.title} ({command.name})" == str(commands_from_db[i])


@pytest.mark.django_db
def test_get_command(command_factory):
    commands = command_factory(_quantity=2)

    command = Command.objects.get(id=commands[0].id)
    assert command.name == commands[0].name


@pytest.mark.django_db
def test_create_command():
    command_name = 'test_create_command'
    command = Command.objects.create(action=Action.ADD,
                                     name=command_name,
                                     title=get_random_string(10),
                                     prefix=get_random_string(10))

    command = Command.objects.get(id=command.id)
    assert command.name == command_name


@pytest.mark.parametrize(['attribute', 'default_value'],
                         (('action', Action.ADD_NEXT),))
@pytest.mark.django_db
def test_constraints_default_create_command(attribute, default_value):
    command = Command.objects.create(name=get_random_string(10),
                                     title=get_random_string(10),
                                     prefix=get_random_string(10))

    command = Command.objects.get(id=command.id)
    assert command.__getattribute__(attribute) == default_value


@pytest.mark.parametrize('attribute',
                         ('name',
                          'title',))
@pytest.mark.django_db
def test_constraints_not_null_create_command(attribute):
    err_not_null_constraint = 'NOT NULL constraint failed'

    with pytest.raises(IntegrityError) as exc_info:
        Command.objects.create(name=None if attribute == 'name' else get_random_string(10),
                               title=None if attribute == 'title' else get_random_string(10),
                               prefix=None if attribute == 'prefix' else get_random_string(10))
    assert err_not_null_constraint in str(exc_info.value)


@pytest.mark.parametrize('attribute',
                         ('name',
                          'title',
                          'prefix',))
@pytest.mark.django_db
def test_constraints_unique_create_command(attribute):
    err_unique_constraint = 'UNIQUE constraint failed'

    not_unique_text = get_random_string(10)

    Command.objects.create(name=not_unique_text if attribute == 'name' else get_random_string(10),
                           title=not_unique_text if attribute == 'title' else get_random_string(10),
                           prefix=not_unique_text if attribute == 'prefix' else get_random_string(10))

    with pytest.raises(IntegrityError) as exc_info:
        Command.objects.create(name=not_unique_text if attribute == 'name' else get_random_string(10),
                               title=not_unique_text if attribute == 'title' else get_random_string(10),
                               prefix=not_unique_text if attribute == 'prefix' else get_random_string(10))
    assert err_unique_constraint in str(exc_info.value)


@pytest.mark.parametrize(['attribute', 'max_length'],
                         (('name', 256),
                          ('title', 256),
                          ('prefix', 256),))
@pytest.mark.django_db
def test_constraints_max_length_create_command(attribute, max_length):
    with pytest.raises(ValidationError) as exc_info:
        command = Command(
            name=get_random_string(max_length + 1) if attribute == 'name' else get_random_string(max_length - 1),
            title=get_random_string(max_length + 1) if attribute == 'title' else get_random_string(max_length - 1),
            prefix=get_random_string(max_length + 1) if attribute == 'prefix' else get_random_string(max_length - 1))
        command.full_clean()
    assert str(max_length) in str(exc_info.value)


@pytest.mark.django_db
def test_update_command(command_factory):
    command_name = 'test_create_command'
    command = command_factory(_quantity=1)[0]

    command = Command.objects.get(id=command.id)
    assert command.name != command_name

    command.name = command_name
    command.save()

    command = Command.objects.get(id=command.id)
    assert command.name == command_name


@pytest.mark.django_db
def test_delete_command(command_factory):
    command_factory(_quantity=1)

    commands = Command.objects.all()
    assert len(commands) == 1

    commands[0].delete()

    commands = Command.objects.all()
    assert len(commands) == 0
