import webview
import json
import os
import sys
from pathlib import Path

# GOOGLE_API_KEY = "YOUR_API_KEY_HERE"

# Data stored next to the app
DATA_FILE = Path(__file__).parent / "data.json" # Create your own data.json file in the same directory as this script, or it will be created automatically when you save data.

def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"entries": [], "profile": {}}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

class API:
    def get_data(self):
        return load_data()

    def save_entries(self, entries):
        data = load_data()
        data["entries"] = entries
        save_data(data)
        return True

    def save_profile(self, profile):
        data = load_data()
        data["profile"] = profile
        save_data(data)
        return True

    def export_csv(self):
        data = load_data()
        entries = data.get("entries", [])
        if not entries:
            return {"ok": False, "msg": "No entries to export."}
        csv_path = Path(__file__).parent / "outreach_export.csv"
        headers = ["company","website","contact","email","goal","status","tags","notes","updated"]
        lines = [",".join(headers)]
        for e in entries:
            row = ['"' + str(e.get(h,"")).replace('"','""') + '"' for h in headers]
            lines.append(",".join(row))
        csv_path.write_text("\n".join(lines), encoding="utf-8")
        return {"ok": True, "path": str(csv_path)}

def get_html():
    html_path = Path(__file__).parent / "index.html"
    return html_path.read_text(encoding="utf-8")

if __name__ == "__main__":
    api = API()
    window = webview.create_window(
        title="Cold Outreach Tracker",
        html=get_html(),
        js_api=api,
        width=1200,
        height=750,
        min_size=(900, 600),
        background_color="#ffffff"
    )
    webview.start(debug=False)
