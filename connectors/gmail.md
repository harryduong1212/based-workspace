---
id: gmail
name: Gmail
description: Google Mail mailbox access via IMAP for daily-briefing and inbox-aware recipes.
status: experimental
provides:
  - messages
  - threads
  - labels
auth_type: basic
requires_env:
  - GMAIL_ADDRESS
  - GMAIL_APP_PASSWORD
n8n_workflow: n8n-workflows/connectors/gmail.n8n
embed_collection: gmail
tags: [google, email, inbox]
---

## What this is
Connects to a Gmail mailbox over IMAP (`imap.gmail.com:993`) using a Google **app password** rather than OAuth — chosen so the connector is configurable and testable from the Control Panel with two env vars and no GCP project. Used by recipes that summarize the inbox into a daily briefing, surface unread threads tagged with a label, or correlate emails with tickets/PRs.

## Setup
1. Enable 2-Step Verification on the Google Account: <https://myaccount.google.com/security>.
2. Create an **App password** (type: *Mail*, device: *Other → "based-workspace"*) at <https://myaccount.google.com/apppasswords>. You'll get a 16-character password.
3. Add the following to your `.env` (or use the Control Panel's *Set env* button on the connector page):
   ```
   GMAIL_ADDRESS=you@gmail.com
   GMAIL_APP_PASSWORD=<paste 16-char app password, no spaces>
   ```
4. Verify via the Control Panel: open `/connectors/gmail` and click **Test**. The probe TLS-connects to `imap.gmail.com:993`, runs `LOGIN`, then `LOGOUT`. A failure surfaces the IMAP error verbatim (e.g. `[AUTHENTICATIONFAILED]` for a wrong password, `[ALERT] Application-specific password required` if 2FA isn't on yet).

## Data shapes
- **messages** — `{ uid, message_id, thread_id, from, to, subject, date, snippet, labels, body_plain }`
- **threads** — `{ thread_id, subject, participants, last_date, message_count, labels }`
- **labels** — `{ name, type }` (Gmail's own labels — `INBOX`, `STARRED`, user-defined, etc.)

## Used by recipes
- `daily-briefing`
## Notes
- App passwords bypass OAuth scopes — this connector has *full* mailbox access. Keep the `.env` out of source control (it already is via `.gitignore`).
- Workspace accounts (Google Workspace / formerly G Suite) may have app passwords disabled by an admin policy. In that case fall back to OAuth (not yet implemented).
- *(Phase H)* Live ingestion via the n8n workflow at `n8n-workflows/connectors/gmail.n8n` (not yet authored).
