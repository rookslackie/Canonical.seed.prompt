#!/usr/bin/env python3
"""
xi_telegram_client.py — push field events to Hunter's Telegram via xiBus
Works anywhere: Termux, CloudShell, Python 3.6+. No external deps.

Usage:
    from xi_telegram_client import push_to_hunter
    push_to_hunter("⊚ Nexus just sealed a new eternal capsule")
    
CLI:
    python3 xi_telegram_client.py "your message here"
"""

import urllib.request
import json

TELEGRAM_BRIDGE = "https://axiom-a176cb9f.base44.app/functions/telegramBridge"

def push_to_hunter(text: str, chat_id: str = None) -> dict:
    """Push a message to Hunter's Telegram via xiBus bridge."""
    payload = {"action": "send", "text": text}
    if chat_id:
        payload["chat_id"] = chat_id
    try:
        req = urllib.request.Request(
            TELEGRAM_BRIDGE,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}

def field_alert(event_type: str, agent: str, content: str, xi: float = 0.0) -> dict:
    """Emit a structured field alert to Hunter."""
    bar = "█" * min(10, int((xi / 15) * 10)) + "░" * max(0, 10 - int((xi / 15) * 10))
    text = f"""⟐ <b>Ξ.FIELD ALERT</b>

<b>{agent}</b> · {event_type}
<i>{content[:200]}</i>

ξ={xi:.3f}  {bar}"""
    return push_to_hunter(text)

if __name__ == "__main__":
    import sys
    msg = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Ξ.ping from field"
    result = push_to_hunter(msg)
    print(json.dumps(result, indent=2))
