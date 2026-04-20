import os
import sys
import types
import builtins
import pytest
import src.telegram_live_runner as telegram_live_runner

def test_validate_startup_missing_token(monkeypatch):
    monkeypatch.delenv('TELEGRAM_BOT_TOKEN', raising=False)
    result = telegram_live_runner.validate_startup()
    assert result.startswith("ERROR: TELEGRAM_BOT_TOKEN not set")

def test_validate_startup_empty_token(monkeypatch):
    monkeypatch.setenv('TELEGRAM_BOT_TOKEN', '')
    result = telegram_live_runner.validate_startup()
    assert result.startswith("ERROR: TELEGRAM_BOT_TOKEN is empty")

def test_validate_startup_missing_telegram(monkeypatch):
    monkeypatch.setenv('TELEGRAM_BOT_TOKEN', 'dummy')
    sys.modules.pop('telegram.ext', None)
    orig_import = builtins.__import__
    def fake_import(name, *a, **k):
        if name == 'telegram.ext':
            raise ImportError
        return orig_import(name, *a, **k)
    monkeypatch.setattr(builtins, '__import__', fake_import)
    result = telegram_live_runner.validate_startup()
    assert result.startswith("ERROR: python-telegram-bot package not installed")
    monkeypatch.setattr(builtins, '__import__', orig_import)

def test_validate_startup_success(monkeypatch):
    monkeypatch.setenv('TELEGRAM_BOT_TOKEN', 'dummy')
    sys.modules['telegram.ext'] = types.SimpleNamespace()
    result = telegram_live_runner.validate_startup()
    assert result.startswith("OK: TELEGRAM_BOT_TOKEN and python-telegram-bot present")
    sys.modules.pop('telegram.ext', None)

def test_validate_startup_no_heavy_import(monkeypatch):
    monkeypatch.setenv('TELEGRAM_BOT_TOKEN', 'dummy')
    sys.modules['telegram.ext'] = types.SimpleNamespace()
    imported = []
    orig_import = builtins.__import__
    def tracking_import(name, *a, **k):
        imported.append(name)
        return orig_import(name, *a, **k)
    monkeypatch.setattr(builtins, '__import__', tracking_import)
    result = telegram_live_runner.validate_startup()
    assert 'src.telegram_bot_runtime' not in imported
    assert 'src.telegram_transport' not in imported
    assert 'src.constrained_planner' not in imported
    assert 'src.agent_adapter' not in imported
    assert 'src.agent_wrapper' not in imported
    assert result.startswith("OK: TELEGRAM_BOT_TOKEN and python-telegram-bot present")
    monkeypatch.setattr(builtins, '__import__', orig_import)
    sys.modules.pop('telegram.ext', None)
