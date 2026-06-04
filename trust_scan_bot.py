import argparse
import logging
import sys
from pathlib import Path
import importlib.util

LOG = logging.getLogger("trust_scan_bot")


def run_deep():
    try:
        from deep_scan import deep_scan
        # deep_scan doesn't accept a url parameter currently
        return deep_scan()
    except Exception:
        # Try loading by file path when running under test import contexts
        try:
            spec = importlib.util.spec_from_file_location('deep_scan', str(Path(__file__).resolve().parent / 'deep_scan.py'))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod.deep_scan()
        except Exception:
            LOG.exception("Failed running deep scanner")


def run_mohave(url=None):
    try:
        from mohave_audit import mohave_scanner
        # pass through url if provided
        if url:
            return mohave_scanner.run_audit(url=url)
        else:
            return mohave_scanner.run_audit()
    except Exception:
        LOG.exception("Failed running mohave scanner")


SCANNERS = {
    'deep': run_deep,
    'mohave': run_mohave,
}


def discover_scanners(base_dir='.'):
    """Discover files named '*_scanner.py' under base_dir and return a mapping
    of scanner key -> callable. The key format is '<parent>.<module>' when
    the file is inside a folder, otherwise just the module stem.
    """
    mapping = {}
    base = Path(base_dir)
    for f in base.rglob('*_scanner.py'):
        # avoid virtualenv directories
        if 'venv' in f.parts or '.venv' in f.parts or 'site-packages' in f.parts:
            continue
        try:
            key = f"{f.parent.name}.{f.stem}" if f.parent.name != '.' else f.stem
            spec = importlib.util.spec_from_file_location(f"discovered.{f.stem}", str(f))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            # prefer common entry names
            for attr in ('run_audit', 'run', 'scan', 'main'):
                fn = getattr(mod, attr, None)
                if callable(fn):
                    mapping[key] = fn
                    break
        except Exception:
            LOG.exception('Failed to import scanner file: %s', f)
    return mapping


# Discover additional scanners and register them
try:
    discovered = discover_scanners('.')
    for k, v in discovered.items():
        if k in SCANNERS:
            i = 1
            newk = f"{k}_{i}"
            while newk in SCANNERS:
                i += 1
                newk = f"{k}_{i}"
            SCANNERS[newk] = v
        else:
            SCANNERS[k] = v
except Exception:
    LOG.exception('Scanner discovery failed')


def build_parser():
    p = argparse.ArgumentParser(description="Run repository scanners")
    p.add_argument('--scanner', '-s', choices=SCANNERS.keys(), default='deep',
                   help='Which scanner to run')
    p.add_argument('--validate', action='store_true', help='Validate results structure after run')
    p.add_argument('--log-level', default='INFO', help='Logging level')
    p.add_argument('--list', action='store_true', help='List available scanners')
    p.add_argument('--url', help='Optional URL to pass to the scanner')
    p.add_argument('--output', '-o', help='Optional file path to write logs/output')
    p.add_argument('--results', '-r', help='Optional file path to write structured results (json or csv)')
    p.add_argument('--dashboard', help='Optional HTML dashboard output path')
    return p


def main(argv=None):
    argv = argv or sys.argv[1:]
    args = build_parser().parse_args(argv)

    root_level = getattr(logging, args.log_level.upper(), logging.INFO)
    handlers = [logging.StreamHandler()]
    logging.basicConfig(level=root_level,
                        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
                        handlers=handlers)

    if args.output:
        # Attach a file handler for persistent logs/output
        fh = logging.FileHandler(args.output)
        fh.setLevel(root_level)
        fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s'))
        logging.getLogger().addHandler(fh)

    results_path = args.results

    if args.list:
        print('Available scanners:')
        for k in SCANNERS:
            print(f" - {k}")
        return

    LOG.info('Starting scanner: %s', args.scanner)
    runner = SCANNERS.get(args.scanner)
    if not runner:
        LOG.error('Unknown scanner: %s', args.scanner)
        return
    # Pass url option where supported
    result = None
    if args.url:
        try:
            result = runner(args.url)
        except TypeError:
            result = runner()
    else:
        result = runner()

    # Write structured results if requested and available
    if results_path and result is not None:
        try:
            import json, csv
            if results_path.lower().endswith('.json'):
                with open(results_path, 'w', encoding='utf-8') as fh:
                    json.dump({'scanner': args.scanner, 'result': result}, fh, ensure_ascii=False, indent=2)
                LOG.info('Wrote results to %s', results_path)
            elif results_path.lower().endswith('.csv'):
                # Attempt to write a simple CSV if result is a list of dicts
                if isinstance(result, list) and result and isinstance(result[0], dict):
                    keys = sorted({k for d in result for k in d.keys()})
                    with open(results_path, 'w', newline='', encoding='utf-8') as fh:
                        writer = csv.DictWriter(fh, fieldnames=keys)
                        writer.writeheader()
                        for row in result:
                            writer.writerow(row)
                    LOG.info('Wrote results to %s', results_path)
                else:
                    # Fallback: write JSON into CSV file
                    with open(results_path, 'w', encoding='utf-8') as fh:
                        fh.write(str(result))
                    LOG.info('Wrote fallback results to %s', results_path)
            else:
                LOG.error('Unsupported results file extension: %s', results_path)
        except Exception:
            LOG.exception('Failed writing results to %s', results_path)
        else:
            # Optionally validate the written result
            if args.validate:
                        try:
                            # Prefer JSON Schema validation when available
                            schema_path = None
                            if 'mohave' in args.scanner:
                                schema_path = Path('schemas') / 'mohave_schema.json'
                            elif 'deep' in args.scanner:
                                schema_path = Path('schemas') / 'deep_schema.json'

                            if schema_path and schema_path.exists():
                                try:
                                    import jsonschema, json
                                    schema = json.loads(schema_path.read_text(encoding='utf-8'))
                                    jsonschema.validate(instance=result, schema=schema)
                                    LOG.info('JSON Schema validation passed for %s', args.scanner)
                                except Exception as e:
                                    LOG.error('JSON Schema validation failed: %s', e)
                            else:
                                valid, msg = validate_results(args.scanner, result)
                                if not valid:
                                    LOG.error('Result validation failed: %s', msg)
                                else:
                                    LOG.info('Result validation passed')
                        except Exception:
                            LOG.exception('Validation raised an exception')
            # generate dashboard if requested
            if args.dashboard and result is not None:
                try:
                    generate_html_dashboard(args.scanner, result, args.dashboard)
                except Exception:
                    LOG.exception('Failed generating dashboard')
def validate_results(scanner_name, result):
    """Perform lightweight validation of result structures for known scanners.

    Returns (bool, message).
    """
    # mohave returns dict with 'synced' (int) and 'current_live_names' (list)
    if 'mohave' in scanner_name:
        if not isinstance(result, dict):
            return False, 'expected dict for mohave scanner'
        if 'synced' not in result or not isinstance(result.get('synced'), int):
            return False, "missing or invalid 'synced'"
        if 'current_live_names' not in result or not isinstance(result.get('current_live_names'), list):
            return False, "missing or invalid 'current_live_names'"
        return True, 'ok'

    # deep returns list of dicts with 'text' and 'url'
    if 'deep' in scanner_name:
        if not isinstance(result, list):
            return False, 'expected list for deep scanner'
        for i, item in enumerate(result):
            if not isinstance(item, dict):
                return False, f'item {i} not a dict'
            if 'text' not in item or 'url' not in item:
                return False, f'item {i} missing keys'
        return True, 'ok'

    # Generic checks: if list of dicts, ensure keys are consistent
    if isinstance(result, list) and result and isinstance(result[0], dict):
        return True, 'ok (generic list-of-dicts)'
    if isinstance(result, dict):
        return True, 'ok (generic dict)'
    return False, 'unknown result shape'


def generate_html_dashboard(scanner_name, result, outpath):
    """Generate a minimal HTML dashboard summarizing a scanner result."""
    from html import escape
    rows = ''
    summary = ''
    if isinstance(result, list):
        # assume list of dicts
        keys = sorted({k for d in result for k in d.keys()}) if result else []
        header = ''.join(f'<th>{escape(k)}</th>' for k in keys)
        for d in result:
            cells = ''
            for k in keys:
                v = d.get(k, '')
                if isinstance(v, str) and v.startswith('http'):
                    cells += f'<td><a href="{escape(v)}" target="_blank">{escape(v)}</a></td>'
                else:
                    cells += f'<td>{escape(str(v))}</td>'
            rows += f'<tr>{cells}</tr>\n'
        table = f'<table class="results">\n<thead><tr>{header}</tr></thead>\n<tbody>{rows}</tbody></table>'
        summary = f'<p>Items: {len(result)}</p>'
    elif isinstance(result, dict):
        items = ''
        for k, v in result.items():
            items += f'<tr><th>{escape(k)}</th><td>{escape(str(v))}</td></tr>'
        table = f'<table class="results">{items}</table>'
        # small summary
        if 'synced' in result:
            summary = f"<p>Synced: {result.get('synced')}</p>"
    else:
        table = f'<pre>{escape(str(result))}</pre>'

    css = '''
body { font-family: Arial, sans-serif; margin: 20px; }
h1 { font-size: 20px; }
.meta { color: #444; margin-bottom: 8px }
.results { border-collapse: collapse; width: 100%; }
.results th, .results td { border: 1px solid #ddd; padding: 8px; }
.results th { background: #f4f4f4; text-align: left; }
a { color: #1a0dab; }
'''

    html = f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Scanner Dashboard - {escape(scanner_name)}</title>
  <style>{css}</style>
</head>
<body>
  <h1>Scanner: {escape(scanner_name)}</h1>
  <div class="meta">{summary}</div>
  {table}
</body>
</html>
"""
    Path(outpath).write_text(html, encoding='utf-8')
    LOG.info('Wrote dashboard to %s', outpath)


if __name__ == '__main__':
    main()
