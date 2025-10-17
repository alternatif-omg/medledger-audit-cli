# sample_project/generate_pqc_signature.py
import base64
import json
import os

try:
    import oqs
except Exception as e:
    raise SystemExit("liboqs-python (oqs) not installed or failed to import: " + str(e))

ALG = "Dilithium2"
MSG = b"MedLedger test"  # sesuaikan pesan yang ingin kamu verifikasi

with oqs.Signature(ALG) as signer:
    pub, priv = signer.generate_keypair()
    sig = signer.sign(MSG, priv)

def b64(x: bytes) -> str:
    return base64.b64encode(x).decode()

out = {
    "algorithm": ALG,
    "message": b64(MSG),         # base64-encoded message
    "public_key": b64(pub),
    "signature": b64(sig)
}

out_path = os.path.join(os.path.dirname(__file__), "pqc_signature.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)
print("Wrote:", out_path)
