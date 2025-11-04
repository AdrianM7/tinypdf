from flask import Flask, request, jsonify
import io, os, pdfplumber

AUTH_TOKEN = os.getenv("AUTH_TOKEN")  # optional

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify({"ok": True})

@app.post("/text")
def text():
    if AUTH_TOKEN:
        auth = request.headers.get("Authorization", "")
        if auth != f"Bearer {AUTH_TOKEN}":
            return jsonify({"error":"unauthorized"}), 401
    if 'file' not in request.files:
        return jsonify({"error":"file missing"}), 400
    raw = request.files['file'].read()
    if not raw:
        return jsonify({"error":"empty file"}), 400
    pages = []
    with pdfplumber.open(io.BytesIO(raw)) as pdf:
        for i, p in enumerate(pdf.pages, start=1):
            pages.append({"page": i, "text": p.extract_text() or ""})
    return jsonify({"ok": True, "pages": pages})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    # IMPORTANT: bind to 0.0.0.0 and port from $PORT
    app.run(host="0.0.0.0", port=port)
