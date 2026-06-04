from flask import Flask, request, jsonify, send_file
from pathlib import Path
import tempfile
import threading
import time

app = Flask(__name__)

# Import scanners and helper from trust_scan_bot
import trust_scan_bot as tsb

@app.route('/')
def index():
    return "<p>Trust Scan Dashboard Server</p><p>Use /list to see scanners, /run to execute.</p>"

@app.route('/list')
def list_scanners():
    return jsonify(sorted(list(tsb.SCANNERS.keys())))

@app.route('/run', methods=['POST', 'GET'])
def run_scanner():
    scanner = request.values.get('scanner', 'deep')
    url = request.values.get('url')
    dashboard = request.values.get('dashboard')

    runner = tsb.SCANNERS.get(scanner)
    if not runner:
        return jsonify({'error': 'unknown scanner', 'scanner': scanner}), 404

    # run in thread if long-running
    try:
        if url:
            result = runner(url)
        else:
            result = runner()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # optionally generate dashboard and return path
    if dashboard:
        outpath = Path(dashboard)
    else:
        fd, path = tempfile.mkstemp(prefix=f"{scanner}-", suffix='.html')
        outpath = Path(path)
    try:
        tsb.generate_html_dashboard(scanner, result, str(outpath))
    except Exception as e:
        return jsonify({'error': 'failed to generate dashboard', 'detail': str(e)}), 500

    return jsonify({'scanner': scanner, 'result': result, 'dashboard': str(outpath)})

@app.route('/view')
def view_dashboard():
    path = request.values.get('path')
    if not path:
        return jsonify({'error': 'path required'}), 400
    p = Path(path)
    if not p.exists():
        return jsonify({'error': 'file not found'}), 404
    return send_file(str(p))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
