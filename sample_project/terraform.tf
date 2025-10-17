# Terraform MANDAT FINAL: Enforce KMS Isolation
resource "aws_kms_key" "pii_vault_key" {
  description = "KMS key for PII encryption"
  is_enabled  = true
}

# MANDAT FINAL: deny-all baseline
resource "kubernetes_network_policy" "default_deny" {
  metadata {
    name = "deny-all"
  }
  spec {
    pod_selector {}
    policy_types = ["Ingress", "Egress"]
  }
}
