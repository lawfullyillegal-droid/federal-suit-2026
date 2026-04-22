from flask import Flask

app = Flask(__name__)

LOGIN_HTML = """
<!doctype html><html><head><title>Login</title></head>
<body><h1>Login</h1>
<form method="post" action="/login">
  <input type="text" name="username" placeholder="Username"><br>
  <input type="password" name="password" placeholder="Password"><br>
  <button type="submit">Login</button>
</form></body></html>
"""

DASHBOARD_HTML = """
<!doctype html><html><head><title>Dashboard</title></head>
<body><h1>Dashboard</h1><p>Welcome.</p></body></html>
"""

@app.route("/")
def login_page():
    return LOGIN_HTML

@app.route("/dashboard")
def dashboard_page():
    return DASHBOARD_HTML

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
