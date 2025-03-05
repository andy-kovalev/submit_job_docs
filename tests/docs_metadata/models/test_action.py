from docs_metadata.models import Action


def test_get_actions():
    actions = [a.name for a in Action]

    assert len(actions) == 5

    assert 'ADD' in [action for action in actions]
    assert 'ADD_NEXT' in [action for action in actions]
    assert 'END' in [action for action in actions]
    assert 'CANCEL' in [action for action in actions]
    assert 'HELP' in [action for action in actions]
