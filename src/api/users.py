"""User management API with security issues."""
import os
import yaml
import subprocess
from flask import request, jsonify

@app.route("/api/users/export", methods=["GET"])
def export_users():
    format_type = request.args.get("format", "csv")
    # CWE-78: Command injection via format parameter
    output = subprocess.check_output(
        f"python3 export_script.py --format {format_type}", shell=True
    )
    return output

@app.route("/api/users/import", methods=["POST"])
def import_users():
    data = request.get_data()
    # CWE-502: Unsafe YAML deserialization
    config = yaml.load(data, Loader=yaml.FullLoader)
    return jsonify({"imported": len(config.get("users", []))})

@app.route("/api/users/avatar", methods=["POST"])
def upload_avatar():
    url = request.json.get("avatar_url")
    # CWE-918: SSRF - fetching arbitrary URLs
    import requests
    response = requests.get(url)
    filename = url.split("/")[-1]
    # CWE-22: Path traversal in filename
    with open(f"/uploads/{filename}", "wb") as f:
        f.write(response.content)
    return jsonify({"saved": filename})
