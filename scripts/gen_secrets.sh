#!/usr/bin/env bash
# Print random values for the secrets that can be auto-generated.
# Pipes to stdout — does NOT touch .env, so it can't overwrite existing values.
# Copy individual lines and paste into your local .env.
#
# Usage: ./scripts/gen_secrets.sh

set -euo pipefail

# 24 url-safe bytes → ~32 char base64. Plenty of entropy, no shell-quoting woes.
rand_b64() { python3 -c 'import secrets; print(secrets.token_urlsafe(24))'; }
# 32 hex chars = 16 random bytes; n8n's recommended format for the encryption key.
rand_hex() { python3 -c 'import secrets; print(secrets.token_hex(16))'; }

cat <<EOF
# ---- generated $(date -Iseconds) — paste into .env ----
POSTGRES_PASSWORD=$(rand_b64)
N8N_ENCRYPTION_KEY=$(rand_hex)
N8N_USER_MANAGEMENT_JWT_SECRET=$(rand_b64)

# ---- paste-from-source (no auto-generation possible) ----
# N8N_API_KEY            → http://localhost:5678 → Settings → API → Create API Key
#                          (n8n stores the key in its DB; client-generated values won't auth)
# GEMINI_API_KEY         → https://aistudio.google.com/app/apikey
# ANTHROPIC_API_KEY      → https://console.anthropic.com/settings/keys
# GITHUB_TOKEN           → https://github.com/settings/tokens
# GMAIL_APP_PASSWORD     → https://myaccount.google.com/apppasswords
# JIRA_API_TOKEN         → https://id.atlassian.com/manage-profile/security/api-tokens
# BITBUCKET_APP_PASSWORD → https://bitbucket.org/account/settings/app-passwords/
EOF
