import pathlib
import tempfile
import json
import csv
import os


def load_trust_scan_bot():
    import importlib.util
    p = pathlib.Path(__file__).resolve().parents[1] / 'trust_scan_bot.py'
    spec = importlib.util.spec_from_file_location('trust_scan_bot', str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_write_json_and_validate(tmp_path):
    mod = load_trust_scan_bot()
    out = tmp_path / 'results.json'
    # Run dummy scanner via discovered key 'fixtures.dummy_scanner'
    mod.main(['--scanner', 'fixtures.dummy_scanner', '--results', str(out), '--validate'])
    assert out.exists()
    data = json.loads(out.read_text(encoding='utf-8'))
    assert data['scanner'] == 'fixtures.dummy_scanner'
    assert isinstance(data['result'], list)


def test_write_csv(tmp_path):
    mod = load_trust_scan_bot()
    out = tmp_path / 'results.csv'
    mod.main(['--scanner', 'fixtures.dummy_scanner', '--results', str(out)])
    assert out.exists()
    # Check CSV has header and two rows
    with open(out, newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
    assert len(rows) == 2
    assert 'text' in rows[0] and 'url' in rows[0]


def test_validate_with_schema_and_dashboard(tmp_path):
    mod = load_trust_scan_bot()
    # Use deep scanner which has a schema
    out_json = tmp_path / 'deep.json'
    out_html = tmp_path / 'deep.html'
    mod.main(['--scanner', 'deep', '--results', str(out_json), '--dashboard', str(out_html), '--validate'])
    assert out_json.exists()
    assert out_html.exists()
