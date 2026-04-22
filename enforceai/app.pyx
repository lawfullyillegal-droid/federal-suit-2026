from flask import Flask, request, render_template_string, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'enforceai-secret-key-2026'

users = {'test@lawfully.com': 'pass123'}

LOGIN_HTML = """<!DOCTYPE html>
<html><head><title>EnforceAI — Lawfully Illegal</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-black text-white min-h-screen flex items-center justify-center">
<div class="bg-gray-900 p-8 rounded-2xl max-w-md w-full">
<h1 class="text-5xl font-bold text-red-500 text-center mb-2">EnforceAI</h1>
<p class="text-center text-gray-400 mb-2">by Lawfully Illegal</p>
<p class="text-center text-red-500 mb-6">Public Accountability • Private Power</p>
<form method="POST">
<input type="email" name="email" value="test@lawfully.com" class="w-full p-4 bg-gray-800 rounded mb-4">
<input type="password" name="password" value="pass123" class="w-full p-4 bg-gray-800 rounded mb-6">
<button type="submit" class="w-full bg-red-600 py-4 rounded font-bold">LOGIN</button>
</form>
<p class="text-center text-gray-500">Test: test@lawfully.com / pass123</p>
</div></body></html>"""

DASHBOARD_HTML = """<!DOCTYPE html>
<html><head><title>Dashboard — Lawfully Illegal</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-black text-white">
<nav class="bg-gray-900 p-4 flex justify-between items-center">
<h1 class="text-2xl font-bold text-red-500">EnforceAI</h1>
<span class="text-gray-400 text-sm">by Lawfully Illegal</span>
<a href="/logout" class="text-red-400">Logout</a>
</nav>
<div class="max-w-2xl mx-auto p-6">
<h2 class="text-3xl mb-8">Generate Remedy</h2>
<form method="POST" action="/new_case">
<input name="title" placeholder="Case Title (e.g. My First Trust Case)" class="w-full p-4 bg-gray-800 rounded mb-4">
<input name="statute" placeholder="Statute or Issue (e.g. 14th Amendment)" class="w-full p-4 bg-gray-800 rounded mb-6">
<button type="submit" class="w-full bg-red-600 py-5 rounded font-bold text-lg">GENERATE REMEDY</button>
</form>
</div></body></html>"""

@app.route('/')
def home(): return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        pw = request.form.get('password')
        if email in users and users[email] == pw:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        return render_template_string(LOGIN_HTML)
    return render_template_string(LOGIN_HTML)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'): return redirect(url_for('login'))
    return render_template_string(DASHBOARD_HTML)

@app.route('/new_case', methods=['POST'])
def new_case():
    if not session.get('logged_in'): return redirect(url_for('login'))
    title = request.form.get('title', 'New Case')
    statute = request.form.get('statute', 'Unknown Statute')
    
    # FULL GROK-LEVEL REMEDY — structured, actionable, on-brand
    remedy = f"""✅ LAW FULLY ILLEGAL REMEDY GENERATED

**Case:** {title}
**Statute / Issue:** {statute}

**Step-by-Step Enforcement Plan:**
1. Revoke consent & declare private express trust status under common law.
2. File Notice of Affidavit of Truth & Revocation of 14th Amendment Citizenship.
3. Record UCC-1 Financing Statement naming yourself as Secured Party.
4. Serve certified notice on the offending party/agency via USPS Certified Mail + Return Receipt.

**Sample Affidavit Template (copy & use):**
I, [Your Full Name], sui juris, do solemnly declare that I revoke all consent to any implied contract with the corporate UNITED STATES or its agencies. I am a living man/woman, not a 14th Amendment citizen. All rights reserved without prejudice. UCC 1-308.

Signed: ____________________
Date: ____________________

Full templates + more remedies available on GitHub: https://github.com/lawfullyillegal-droid
Visit my full platform: https://lawfullyillegal.art"""

    return f"""<div style="background:#111; padding:30px; border-radius:12px; max-width:700px; margin:20px auto; color:#fff;">
<h2 style="color:#ff0000;">Case Saved: {title}</h2>
<pre style="white-space:pre-wrap; font-size:16px;">{remedy}</pre>
<br><a href="/dashboard" style="color:#ff0000; font-weight:bold;">← Back to Dashboard</a>
</div>"""

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

