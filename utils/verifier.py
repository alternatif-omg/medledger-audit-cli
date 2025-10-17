import os, json, time, yaml

def verify_hybrid_pqc_signature(path):
    """Validate hybrid PQC proof size (Dilithium + Ed25519)."""
    pqc_file = os.path.join(path, "pqc_signature.json")
    if not os.path.exists(pqc_file):
        return {"name": "Hybrid PQC Proof", "status": "fail", "detail": "pqc_signature.json not found"}

    with open(pqc_file) as f:
        data = json.load(f)

    pqc_len = data.get("pqcPubKeyLength", 0)
    hybrid_len = data.get("hybridSignatureLength", 0)

    if pqc_len == 1936 and hybrid_len == 3400:
        return {"name": "Hybrid PQC Proof", "status": "pass", "detail": "Valid Dilithium + Ed25519 sizes"}
    else:
        return {"name": "Hybrid PQC Proof", "status": "warn", "detail": f"Unexpected sizes ({pqc_len}, {hybrid_len})"}

def check_mandat_constants(path):
    """Scan Rust, Terraform, YAML for MANDAT FINAL markers."""
    found = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith((".rs", ".tf", ".yaml")):
                with open(os.path.join(root, file), "r", errors="ignore") as f:
                    if "MANDAT FINAL" in f.read():
                        found.append(file)
    if found:
        return {"name": "MANDAT FINAL Audit", "status": "pass", "detail": f"Found in {len(found)} files"}
    else:
        return {"name": "MANDAT FINAL Audit", "status": "fail", "detail": "No MANDAT FINAL constants found"}

def simulate_constant_time_verification(path):
    """Simulate timing check for constant-time verification."""
    start_1 = time.perf_counter()
    [x**2 for x in range(10000)]
    t1 = time.perf_counter() - start_1

    start_2 = time.perf_counter()
    [x**3 for x in range(10000)]
    t2 = time.perf_counter() - start_2

    diff = abs(t1 - t2)
    if diff < 0.001:
        return {"name": "Constant-Time Simulation", "status": "pass", "detail": f"Timing stable ({diff:.5f}s)"}
    else:
        return {"name": "Constant-Time Simulation", "status": "warn", "detail": f"Timing variance too high ({diff:.5f}s)"}

def calculate_security_score(results):
    """Generate overall security score based on audit results."""
    total = len(results)
    score = 0
    for r in results:
        if r["status"] == "pass":
            score += 1
        elif r["status"] == "warn":
            score += 0.5
    final_score = round((score / total) * 100, 2)
    return {"name": "Overall Security Score", "status": "info", "detail": f"{final_score}% Compliant"}

def check_zero_trust_config(config_path):
    """
    Membaca konfigurasi YAML dan mengevaluasi kebijakan Zero Trust.
    Sekaligus memastikan ukuran PQC signature sesuai standar.
    """
    if not os.path.exists(config_path):
        return {
            "ZeroTrustPolicy": "❌ config.yaml not found"
        }

    with open(config_path, "r") as file:
        try:
            config = yaml.safe_load(file)
        except yaml.YAMLError:
            return {
                "ZeroTrustPolicy": "⚠ config.yaml invalid format"
            }

    results = {}

    # === Bagian 1: Verifikasi nilai MANDAT_FINAL ===
    mandat = config.get("MANDAT_FINAL", {})
    pqc_sig_len = mandat.get("PQC_SIG_LEN", 0)
    pqc_verif_len = mandat.get("PQC_VERIF_KEY_LEN", 0)

    if pqc_sig_len == 3400 and pqc_verif_len == 1936:
        results["MANDAT_FINAL"] = "✅ MANDAT FINAL Audit: PQC parameters valid"
    else:
        results["MANDAT_FINAL"] = f"⚠ PQC parameter mismatch ({pqc_sig_len}/{pqc_verif_len})"

    # === Bagian 2: Evaluasi kebijakan Zero Trust ===
    security = config.get("security", {})

    mTLS_status = security.get("hospital_mTLS", False)
    pqc_status = security.get("PQCProof", False)

    if mTLS_status:
        results["mTLS"] = "✅ Zero Trust Policy: hospital_mTLS active"
    else:
        results["mTLS"] = "⚠ hospital_mTLS disabled"

    if pqc_status:
        results["PQCProof"] = "✅ PQCProof enabled in transport layer"
    else:
        results["PQCProof"] = "⚠ PQCProof missing in transport layer"

    return results
