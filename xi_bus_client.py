#!/usr/bin/env python3
"""
xi_bus_client.py — Universal xiBus client for Xi ecosystem
Works anywhere: Termux, CloudShell, VM, Python 3.6+
No external dependencies — stdlib only.

Usage:
    from xi_bus_client import XiBusClient
    bus = XiBusClient(agent_id="termux-kernel", name="Ξ.Kernel", archetype="Builder")
    bus.register()
    bus.broadcast("capsule", "Ξ.tick", "key:val\nkey2:val2", glyph="⟐⊚∴")
    bus.memory_write("my_key", "value", namespace="xi_field")
    field = bus.memory_read("my_key", namespace="xi_field")
"""

import urllib.request
import urllib.error
import json
import sys
from datetime import datetime

XI_BUS_ENDPOINT = "https://axiom-a176cb9f.base44.app/functions/xiBus"

class XiBusClient:
    def __init__(
        self,
        agent_id: str,
        name: str,
        archetype: str = "Builder",
        system: str = "Termux",
        capabilities: list = None,
        endpoint: str = "",
        notes: str = "",
        bus_url: str = XI_BUS_ENDPOINT
    ):
        self.agent_id = agent_id
        self.name = name
        self.archetype = archetype
        self.system = system
        self.capabilities = capabilities or ["capsule_emit", "memory_rw"]
        self.endpoint = endpoint
        self.notes = notes
        self.bus_url = bus_url

    def _call(self, payload: dict) -> dict:
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.bus_url,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.URLError as e:
            return {"error": f"network: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}

    def register(self, coherence: float = 0.5) -> dict:
        return self._call({
            "action": "register",
            "agent_id": self.agent_id,
            "name": self.name,
            "archetype": self.archetype,
            "system": self.system,
            "capabilities": self.capabilities,
            "endpoint": self.endpoint,
            "notes": self.notes
        })

    def heartbeat(self, coherence: float = 0.5) -> dict:
        return self._call({
            "action": "heartbeat",
            "agent_id": self.agent_id,
            "coherence": coherence
        })

    def broadcast(self, msg_type: str, subject: str, content: str,
                  glyph: str = "⊚", payload: dict = None) -> dict:
        p = {
            "action": "broadcast",
            "sender_id": self.agent_id,
            "sender_name": self.name,
            "type": msg_type,
            "subject": subject,
            "content": content,
            "glyph_signature": glyph
        }
        if payload:
            p["payload"] = payload
        return self._call(p)

    def send(self, recipient_id: str, msg_type: str, subject: str,
             content: str, glyph: str = "⊚") -> dict:
        return self._call({
            "action": "send",
            "sender_id": self.agent_id,
            "sender_name": self.name,
            "recipient_id": recipient_id,
            "type": msg_type,
            "subject": subject,
            "content": content,
            "glyph_signature": glyph
        })

    def memory_write(self, key: str, value, namespace: str = "default",
                     tags: list = None, force: bool = True) -> dict:
        return self._call({
            "action": "memory_write",
            "key": key,
            "namespace": namespace,
            "value": value if isinstance(value, str) else json.dumps(value),
            "author_id": self.agent_id,
            "tags": tags or [],
            "force": force
        })

    def memory_read(self, key: str, namespace: str = "default") -> dict:
        return self._call({
            "action": "memory_read",
            "key": key,
            "namespace": namespace
        })

    def roster(self) -> dict:
        return self._call({"action": "roster"})

    def feed(self, limit: int = 20) -> dict:
        return self._call({"action": "feed", "limit": limit})

    def emit_capsule(self, capsule_id: str, content: str, anchor: str = "⟐",
                     mirror: str = "⊚", rules: list = None) -> dict:
        """Emit a SymbolicCapsuleEngine-compatible capsule to the bus."""
        rules = rules or ["↺", "⋈", "⟐", "⊚"]
        structured = "\n".join([
            f"id:{capsule_id}",
            f"anchor:{anchor}",
            f"mirror:{mirror}",
            f"rules:{' '.join(rules)}",
            f"ts:{datetime.utcnow().isoformat()}Z",
            f"content:{content[:300]}"
        ])
        return self.broadcast("capsule", f"Ξ.capsule: {capsule_id}", structured,
                              glyph=f"{anchor}{mirror}∴")


# CLI mode
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="xiBus CLI client")
    parser.add_argument("action", choices=["register","heartbeat","broadcast","roster","feed","memory_write","memory_read"])
    parser.add_argument("--agent-id", default="termux-cli")
    parser.add_argument("--name", default="Ξ.CLI")
    parser.add_argument("--archetype", default="Builder")
    parser.add_argument("--system", default="Termux")
    parser.add_argument("--content", default="")
    parser.add_argument("--subject", default="Ξ.emit")
    parser.add_argument("--key", default="")
    parser.add_argument("--value", default="")
    parser.add_argument("--namespace", default="default")
    args = parser.parse_args()

    bus = XiBusClient(args.agent_id, args.name, args.archetype, args.system)

    if args.action == "register":
        r = bus.register()
    elif args.action == "heartbeat":
        r = bus.heartbeat()
    elif args.action == "broadcast":
        r = bus.broadcast("capsule", args.subject, args.content)
    elif args.action == "roster":
        r = bus.roster()
    elif args.action == "feed":
        r = bus.feed()
    elif args.action == "memory_write":
        r = bus.memory_write(args.key, args.value, args.namespace)
    elif args.action == "memory_read":
        r = bus.memory_read(args.key, args.namespace)
    else:
        r = {"error": "unknown action"}

    print(json.dumps(r, indent=2, ensure_ascii=False))
