#!/usr/bin/env python3
"""Simple web UI for Burmese grapheme to phoneme inference."""

from __future__ import annotations

import os

from flask import Flask, jsonify, request, send_from_directory

from translate import list_models, translate

app = Flask(__name__, static_folder="static", static_url_path="")


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/models")
def api_models():
    models = list_models()
    default_id = os.environ.get("DEFAULT_MODEL", "baseline.transformer.myph") # best BLEU score so far
    default = next((m for m in models if m["id"] == default_id), models[0] if models else None)
    return jsonify({"models": models, "default": default})


@app.post("/api/translate")
def api_translate():
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    model_id = (payload.get("model") or "").strip()

    if not text:
        return jsonify({"error": "Enter Burmese text to translate."}), 400
    if not model_id:
        return jsonify({"error": "Select a model."}), 400

    try:
        result = translate(text, model_id)
        return jsonify(result)
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "7860"))
    app.run(host=host, port=port, debug=False)
