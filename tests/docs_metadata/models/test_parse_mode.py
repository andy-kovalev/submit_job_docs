from docs_metadata.models import ParseMode


def test_get_parse_modes():
    actions = [p.name for p in ParseMode]

    assert len(actions) == 3

    assert 'MARKDOWN' in [action for action in actions]
    assert 'MARKDOWN_V2' in [action for action in actions]
    assert 'HTML' in [action for action in actions]
