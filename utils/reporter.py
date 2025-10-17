from rich.console import Console
import json
from jinja2 import Environment, FileSystemLoader, Template
import os
from datetime import datetime

console = Console()

def print_report(results):
    for r in results:
        if r["status"] == "pass":
            icon, style = "✅", "green"
        elif r["status"] == "warn":
            icon, style = "⚠️", "yellow"
        elif r["status"] == "info":
            icon, style = "ℹ️", "cyan"
        else:
            icon, style = "❌", "red"

        console.print(f"{icon} [bold]{r['name']}[/bold]: {r['detail']}", style=style)


def save_json_report(results, filename="audit_report.json"):
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    console.print(f"\n📄 [cyan]Report saved to {filename}[/cyan]")

import os
import datetime
from jinja2 import Template

def generate_html_report(audit_report, output_path="reports/audit_report.html"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    template = Template("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>MedLedger Security Audit Report</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f9fafb; margin: 0; padding: 20px; color: #111827; }
            h1 { color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px; }
            .section { background: white; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
            .title { font-size: 18px; font-weight: 600; margin-bottom: 10px; display: flex; align-items: center; }
            .pass { color: #16a34a; }
            .fail { color: #dc2626; }
            .info { color: #2563eb; }
            .warning { color: #ca8a04; }
            .score { font-size: 20px; font-weight: bold; color: #fff; background: #16a34a; padding: 8px 16px; border-radius: 8px; display: inline-block; }
            .zt-item { padding: 5px 0; }
        </style>
    </head>
    <body>
        <h1>🔍 MedLedger Security Audit Report</h1>
        <p><b>Generated on:</b> {{ timestamp }}</p>
        <p>📂 <b>Project:</b> {{ project }}</p>

        <div class="section">
            <div class="title">🧱 Core Audit</div>
            {% for item in results %}
                {% if item.status == 'pass' %}
                    <p class="pass">✅ <b>{{ item.name }}</b>: {{ item.detail }}</p>
                {% elif item.status == 'fail' %}
                    <p class="fail">❌ <b>{{ item.name }}</b>: {{ item.detail }}</p>
                {% elif item.status == 'warning' %}
                    <p class="warning">⚠️ <b>{{ item.name }}</b>: {{ item.detail }}</p>
                {% else %}
                    <p class="info">ℹ️ <b>{{ item.name }}</b>: {{ item.detail }}</p>
                {% endif %}
            {% endfor %}
        </div>

        <div class="section">
            <div class="title">🛡️ Zero Trust Summary</div>
            <div class="zt-item">{{ zeroTrust.MANDAT_FINAL }}</div>
            <div class="zt-item">{{ zeroTrust.mTLS }}</div>
            <div class="zt-item">{{ zeroTrust.PQCProof }}</div>
        </div>

        <div class="section">
            <div class="title">📊 Final Score</div>
            <span class="score">{{ final_score }}</span>
        </div>
    </body>
    </html>
    """)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    project_name = os.path.basename(os.getcwd())

    # Ambil skor terakhir dari hasil (biasanya elemen terakhir)
    final_score = "Unknown"
    for r in audit_report["results"]:
        if r["name"] == "Overall Security Score":
            final_score = r["detail"]

    html_output = template.render(
        timestamp=timestamp,
        project=project_name,
        results=audit_report["results"],
        zeroTrust=audit_report.get("ZeroTrust", {}),
        final_score=final_score
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_output)
    print(f"✅ HTML report generated at: {output_path}")
