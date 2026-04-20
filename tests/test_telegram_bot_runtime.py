from src.telegram_bot_runtime import process_update

def test_supported_query():
    update = {'message': {'text': 'What is the annual limit for Remedy 04?'}}
    out = process_update(update)
    assert isinstance(out, str)
    assert "Intent: plan_core" in out
    assert "Remedy 04" in out

def test_unsupported_query():
    update = {'message': {'text': 'Tell me about Remedy 99'}}
    out = process_update(update)
    assert isinstance(out, str)
    assert "unsupported" in out.lower() or "no supported plan" in out.lower()

def test_empty_text():
    update = {'message': {'text': ''}}
    out = process_update(update)
    assert isinstance(out, str)
    assert "didn't receive a valid question" in out.lower()

def test_no_text_key():
    update = {'message': {}}
    out = process_update(update)
    assert isinstance(out, str)
    assert "didn't receive a valid question" in out.lower()

def test_irrelevant_update():
    assert process_update({}) is None
    assert process_update({'not_message': {}}) is None
    assert process_update({'message': None}) is None
    assert process_update(None) is None
