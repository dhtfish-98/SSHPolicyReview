"""Offline review of explicit sshd_config declarations and unresolved scopes."""
from __future__ import annotations
import shlex

SENSITIVE = {"permitrootlogin", "passwordauthentication", "permitemptypasswords", "x11forwarding"}


def review_text(text: str) -> list[dict[str, str]]:
    findings = []
    effective = {}
    scope = 0
    for number, raw in enumerate(text.splitlines(), 1):
        try:
            parts = shlex.split(raw, comments=True, posix=True)
        except ValueError as exc:
            raise ValueError(f"invalid quoting on line {number}") from exc
        if not parts:
            continue
        first = parts.pop(0)
        if "=" in first:
            key, inline = first.split("=", 1)
            if inline:
                parts.insert(0, inline)
        else:
            key = first
            if parts and parts[0] == "=":
                parts.pop(0)
        key = key.lower()
        if not key or not parts:
            raise ValueError(f"invalid directive on line {number}")
        if key == "include":
            findings.append({"rule": "unresolved-include", "location": f"line {number}", "note": "Included files are not opened; review them separately"})
        if key == "match":
            scope += 1
            findings.append({"rule": "match-scope-review", "location": f"line {number}", "note": "Conditional settings are reviewed as declarations without evaluating the predicate"})
            continue
        if key not in SENSITIVE:
            continue
        permitted = {"yes", "no", "prohibit-password", "without-password", "forced-commands-only"} if key == "permitrootlogin" else {"yes", "no"}
        if len(parts) != 1 or parts[0] not in permitted:
            raise ValueError(f"invalid selected setting on line {number}")
        identity = (scope, key)
        if identity not in effective:
            effective[identity] = (parts[0], number)
    for (scope, key), (value, number) in effective.items():
        if value == "yes":
            note = "Review this explicit global setting" if scope == 0 else "Review this explicit conditional setting; effective applicability is unresolved"
            findings.append({"rule": key, "location": f"line {number}", "note": note})
    return findings
