"""Offline review of explicit global sshd_config declarations."""

from __future__ import annotations

SENSITIVE = {
    "permitrootlogin": {"yes"},
    "passwordauthentication": {"yes"},
    "permitemptypasswords": {"yes"},
    "x11forwarding": {"yes"},
}


def review_text(text: str) -> list[dict[str, str]]:
    findings = []
    effective = {}
    in_match = False
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            raise ValueError(f"invalid directive on line {number}")
        key, value = parts[0].lower(), parts[1].strip().lower()
        if key == "match":
            in_match = True
        if in_match:
            continue  # Match rules need server-aware effective-config evaluation.
        if key not in effective:
            effective[key] = (value, number)  # sshd uses the first global value.
    for key, risky in SENSITIVE.items():
        if key in effective and effective[key][0] in risky:
            findings.append({"rule": key, "location": f"line {effective[key][1]}", "note": "Review this explicit global setting"})
    return findings
