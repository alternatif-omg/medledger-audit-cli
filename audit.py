import click
import json
import os
from utils import reporter
from utils.verifier import (
    verify_hybrid_pqc_signature,
    check_mandat_constants,
    simulate_constant_time_verification,
    calculate_security_score,
    check_zero_trust_config
)
from utils.reporter import print_report, save_json_report, generate_html_report


@click.command()
@click.option("--path", default="sample_project", help="Path to project folder")
@click.option("--report", default=None, type=click.Choice(["json", "html"]), help="Output report format")
def main(path, report):
    print(f"\n🔍 Running MedLedger Security Audit on: {path}\n")

    # === 1️⃣ Jalankan semua tahap audit utama ===
    results = []
    results.append(verify_hybrid_pqc_signature(path))
    results.append(check_mandat_constants(path))
    results.append(simulate_constant_time_verification(path))
    results.append(calculate_security_score(results))

    # === 2️⃣ Jalankan audit Zero Trust ===
    zt_results = check_zero_trust_config(f"{path}/config.yaml")

    print(zt_results["MANDAT_FINAL"])
    print(zt_results["mTLS"])
    print(zt_results["PQCProof"])

    # === 3️⃣ Gabungkan semua hasil ke satu laporan ===
    audit_report = {
        "results": results,
        "ZeroTrust": zt_results
    }

    # === 4️⃣ Cetak ke terminal ===
    print_report(results)

    # === 5️⃣ Simpan laporan JSON ===
    save_json_report(audit_report)

    # === 6️⃣ Jika diminta HTML, generate dari JSON terbaru ===
    if report == "html":
        # Pastikan JSON sudah tersimpan sebelum generate HTML
        if os.path.exists("audit_report.json"):
            with open("audit_report.json", "r", encoding="utf-8") as f:
                loaded_data = json.load(f)
            generate_html_report(loaded_data, output_path="reports/audit_report.html")
        else:
            print("⚠️ Warning: audit_report.json not found, skipping HTML generation.")

    print("\n✅ Audit complete! Reports are ready.\n")


if __name__ == "__main__":
    main()
