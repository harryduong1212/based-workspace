"""Live probes for connectors — actually try the credentials, not just check
that env vars are non-empty.

A probe is a zero-arg callable that returns a `ProbeOutcome`. It's run by the
`/connectors/{id}/test` route *after* the env-var presence check has passed.
Probes use stdlib only and impose a hard timeout so a stuck network call can
never block the request thread for long.

Adding a probe: write the function, register it in `PROBES`. The UI will
automatically render its outcome on the next click of the Test button.
"""
from __future__ import annotations

import base64
import imaplib
import json
import os
import socket
import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Callable


_IMAP_TIMEOUT_SECONDS = 8.0
_HTTP_TIMEOUT_SECONDS = 8.0
_USER_AGENT = "based-workspace-control-panel/0.1"


@dataclass(frozen=True)
class ProbeOutcome:
    ok: bool
    message: str


def _probe_gmail() -> ProbeOutcome:
    address = os.environ.get("GMAIL_ADDRESS", "").strip()
    password = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
    if not address or not password:
        return ProbeOutcome(ok=False, message="GMAIL_ADDRESS / GMAIL_APP_PASSWORD not set in process env.")

    imap: imaplib.IMAP4_SSL | None = None
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com", 993, timeout=_IMAP_TIMEOUT_SECONDS)
        imap.login(address, password)
        try:
            imap.logout()
        except Exception:
            pass
        return ProbeOutcome(ok=True, message=f"IMAP login succeeded for {address}.")
    except imaplib.IMAP4.error as e:
        # Wrong password, 2FA-required, app-password-required, etc. Gmail's
        # message is the most useful diagnostic the user can get, surface it.
        return ProbeOutcome(ok=False, message=f"IMAP login rejected: {_imap_error_text(e)}")
    except (socket.timeout, TimeoutError):
        return ProbeOutcome(ok=False, message=f"Timed out after {_IMAP_TIMEOUT_SECONDS:.0f}s connecting to imap.gmail.com:993.")
    except (ssl.SSLError, socket.gaierror, OSError) as e:
        return ProbeOutcome(ok=False, message=f"Network error: {e}")
    finally:
        if imap is not None:
            try:
                imap.shutdown()
            except Exception:
                pass


def _imap_error_text(err: BaseException) -> str:
    args = getattr(err, "args", ())
    if args and isinstance(args[0], (bytes, bytearray)):
        try:
            return args[0].decode("utf-8", errors="replace")
        except Exception:
            return repr(args[0])
    return str(err) or err.__class__.__name__


def _probe_github() -> ProbeOutcome:
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        return ProbeOutcome(ok=False, message="GITHUB_TOKEN not set in process env.")

    req = urllib.request.Request(
        "https://api.github.com/user",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": _USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=_HTTP_TIMEOUT_SECONDS) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="replace"))
        login = payload.get("login") or "(no login field in response)"
        return ProbeOutcome(ok=True, message=f"GitHub /user authenticated as {login}.")
    except urllib.error.HTTPError as e:
        # GitHub returns a JSON {"message": "..."} body for auth failures —
        # surface that text directly so the user knows whether it's a bad
        # token, expired token, or scope issue.
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")
            parsed = json.loads(body)
            if isinstance(parsed, dict) and "message" in parsed:
                body = str(parsed["message"])
        except Exception:
            pass
        return ProbeOutcome(ok=False, message=f"GitHub /user returned HTTP {e.code}: {body or e.reason}")
    except urllib.error.URLError as e:
        reason = e.reason if isinstance(e.reason, str) else str(e.reason)
        return ProbeOutcome(ok=False, message=f"Network error: {reason}")
    except (socket.timeout, TimeoutError):
        return ProbeOutcome(ok=False, message=f"Timed out after {_HTTP_TIMEOUT_SECONDS:.0f}s contacting api.github.com.")


def _probe_jira() -> ProbeOutcome:
    base_url = os.environ.get("JIRA_BASE_URL", "").strip().rstrip("/")
    email = os.environ.get("JIRA_EMAIL", "").strip()
    token = os.environ.get("JIRA_API_TOKEN", "").strip()
    if not base_url or not email or not token:
        return ProbeOutcome(ok=False, message="JIRA_BASE_URL / JIRA_EMAIL / JIRA_API_TOKEN not set in process env.")

    auth_str = f"{email}:{token}"
    auth_b64 = base64.b64encode(auth_str.encode("utf-8")).decode("ascii")

    req = urllib.request.Request(
        f"{base_url}/rest/api/3/myself",
        headers={
            "Authorization": f"Basic {auth_b64}",
            "Accept": "application/json",
            "User-Agent": _USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=_HTTP_TIMEOUT_SECONDS) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="replace"))
        display_name = payload.get("displayName") or email
        return ProbeOutcome(ok=True, message=f"Jira authenticated successfully as {display_name}.")
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        return ProbeOutcome(ok=False, message=f"Jira returned HTTP {e.code}: {body or e.reason}")
    except urllib.error.URLError as e:
        reason = e.reason if isinstance(e.reason, str) else str(e.reason)
        return ProbeOutcome(ok=False, message=f"Network error: {reason}")
    except (socket.timeout, TimeoutError):
        return ProbeOutcome(ok=False, message=f"Timed out after {_HTTP_TIMEOUT_SECONDS:.0f}s contacting Jira.")


def _probe_bitbucket() -> ProbeOutcome:
    username = os.environ.get("BITBUCKET_USERNAME", "").strip()
    password = os.environ.get("BITBUCKET_APP_PASSWORD", "").strip()
    if not username or not password:
        return ProbeOutcome(ok=False, message="BITBUCKET_USERNAME / BITBUCKET_APP_PASSWORD not set in process env.")

    auth_str = f"{username}:{password}"
    auth_b64 = base64.b64encode(auth_str.encode("utf-8")).decode("ascii")

    req = urllib.request.Request(
        "https://api.bitbucket.org/2.0/user",
        headers={
            "Authorization": f"Basic {auth_b64}",
            "Accept": "application/json",
            "User-Agent": _USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=_HTTP_TIMEOUT_SECONDS) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="replace"))
        display_name = payload.get("display_name") or username
        return ProbeOutcome(ok=True, message=f"Bitbucket authenticated successfully as {display_name}.")
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        return ProbeOutcome(ok=False, message=f"Bitbucket returned HTTP {e.code}: {body or e.reason}")
    except urllib.error.URLError as e:
        reason = e.reason if isinstance(e.reason, str) else str(e.reason)
        return ProbeOutcome(ok=False, message=f"Network error: {reason}")
    except (socket.timeout, TimeoutError):
        return ProbeOutcome(ok=False, message=f"Timed out after {_HTTP_TIMEOUT_SECONDS:.0f}s contacting Bitbucket.")


PROBES: dict[str, Callable[[], ProbeOutcome]] = {
    "gmail": _probe_gmail,
    "github": _probe_github,
    "jira": _probe_jira,
    "bitbucket": _probe_bitbucket,
}


def has_probe(connector_id: str) -> bool:
    return connector_id in PROBES


def run_probe(connector_id: str) -> ProbeOutcome | None:
    """Run the registered probe for `connector_id`, or `None` if no probe exists."""
    fn = PROBES.get(connector_id)
    if fn is None:
        return None
    try:
        return fn()
    except Exception as e:  # last-resort guard so the route never 500s
        return ProbeOutcome(ok=False, message=f"Probe raised {type(e).__name__}: {e}")
