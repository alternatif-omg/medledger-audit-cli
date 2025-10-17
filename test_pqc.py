import oqs

with oqs.Signature("Dilithium2") as signer:
    message = b"MedLedger test"

    # Generate keypair — hanya kembalikan public_key
    public_key = signer.generate_keypair()

    # Sign message (pakai secret key internal)
    sig = signer.sign(message)

    # Verify signature
    valid = signer.verify(message, sig, public_key)

print("✅ PQC Signature Verification:", "PASSED" if valid else "FAILED")
