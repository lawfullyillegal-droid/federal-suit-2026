import importlib.util
import pathlib


def load_trust_scan_bot():
    p = pathlib.Path(__file__).resolve().parents[1] / 'trust_scan_bot.py'
    spec = importlib.util.spec_from_file_location('trust_scan_bot', str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_discovery_returns_mapping():
    mod = load_trust_scan_bot()
    discovered = mod.discover_scanners('.')
    assert isinstance(discovered, dict)
    assert len(discovered) >= 1


def test_discovered_callables():
    mod = load_trust_scan_bot()
    discovered = mod.discover_scanners('.')
    for k, fn in discovered.items():
        assert callable(fn), f"Scanner {k} is not callable"
