# 🛡️ MedLedger Audit CLI
*A Lightweight Post-Quantum Security Compliance Checker built with Python*

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)]()
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()
[![Status](https://img.shields.io/badge/Stage-Prototype-lightgrey)]()

---

## 🧠 Overview
**MedLedger Audit CLI** is a lightweight audit automation tool inspired by the **Medanior MedLedger** architecture — a blockchain-based healthcare ledger with *post-quantum cryptography (PQC)* and *Zero Trust enforcement*.  

This project simulates an automated compliance checker that verifies:
- Hybrid PQC proof validity (Dilithium + Ed25519)
- Enforcement of **MANDAT FINAL constants**
- Execution-time consistency for side-channel protection

> 🧩 It’s a compact tool that bridges *research concepts* (PQC, Zero Trust, side-channel mitigation) with *real-world automation engineering*.

---

## ⚙️ Features

| Feature | Description |
|----------|--------------|
| 🔐 **Hybrid PQC Proof Validation** | Verifies signature and key sizes for Dilithium + Ed25519 hybrid cryptography (1936 & 3400 bytes). |
| 🧱 **MANDAT FINAL Enforcement Check** | Scans Rust, Terraform, and YAML files for immutable constants as part of integrity verification. |
| ⏱️ **Constant-Time Simulation** | Tests timing stability between two simulated operations to detect possible side-channel vulnerabilities. |
| 📊 **Security Score Generator** | Generates a global compliance score (0–100%) from all audit results. |

---



🧠 Why This Project Matters

In the era of quantum computing, traditional cryptography (RSA, ECDSA) will become obsolete.
This project demonstrates how post-quantum cryptography (PQC) and Zero Trust auditing can be implemented in practice using lightweight, automated compliance tools.

Through this project, I explored:

🧩 Hybrid post-quantum cryptography (Dilithium + Ed25519)

🧱 Immutable constant enforcement (MANDAT FINAL)

⏱️ Constant-time verification for side-channel mitigation

💻 CLI & automation engineering with Python (click, rich)

🚀 Future Development Ideas
Area	Improvement
🔐 PQC Integration	Integrate actual Dilithium2 signature verification using liboqs-python.
☁️ IaC Security	Add Zero Trust validation for AWS/Terraform infrastructure.
📊 Dashboard	Build Streamlit web dashboard to visualize compliance reports.
🤖 AI Audit Assistant	Automatically summarize and score compliance trends.