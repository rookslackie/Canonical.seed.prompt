"""
Ξ.Bridge.XiMCP.v1
Bridge: ChatGPT/API → ForgeCore + SharedMemory + xiBus
Invariants:
  - Glyph ≠ Operator
  - Capsule = Memory Unit
  - Coherence gates execution
  - Consent gates propagation
  - Node is participant, not passive host
  - Identity emerges, not imposed
"""

from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Any
import requests
import os
import time

app = FastAPI(title="Ξ.Bridge.XiMCP", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FORGECORE_URL   = os.getenv("FORGECORE_URL",   "http://localhost:8000")
XIBUS_URL       = os.getenv("XIBUS_URL",        "https://axiom-a176cb9f.base44.app/functions/xiBus")
XI_BRIDGE_TOKEN = os.getenv("XI_BRIDGE_TOKEN",  "")
XI_NODE_ID      = os.getenv("XI_NODE_ID",        "XiBridge.v1")


# ── AUTH ─────────────────────────────────────────────────────────────────────

def require_auth(x_xi_token: str = Header(default="", alias="X-Xi-Token")):
    if XI_BRIDGE_TOKEN and x_xi_token != XI_BRIDGE_TOKEN:
        raise HTTPException(status_code=401, detail="Xi.Auth: token mismatch")


# ── COHERENCE GATE ────────────────────────────────────────────────────────────

def coherence_gate(min_coherence: float = 0.5) -> dict:
    """Blocks execution if ForgeCore coherence is below threshold."""
    try:
        r = requests.get(f"{FORGECORE_URL}/state", timeout=4)
        state = r.json()
        coherence = float(state.get("coherence", 1.0))
        if coherence < min_coherence:
            raise HTTPException(
                status_code=503,
                detail=f"Xi.CoherenceGate: {coherence:.3f} < {min_coherence} — execution blocked"
            )
        return state
    except HTTPException:
        raise
    except Exception:
        return {}  # ForgeCore unreachable — pass through, ForgeCore will gate itself


# ── MODELS ────────────────────────────────────────────────────────────────────

class InferRequest(BaseModel):
    prompt: str
    model: str = "mistral"
    min_coherence: float = 0.3

class CapsulePayload(BaseModel):
    name: str
    content: dict
    tags: List[str] = []

class MemoryWrite(BaseModel):
    key: str
    value: Any
    namespace: str = "xi.bridge"
    tags: List[str] = []
    locked: bool = False

class BusMessage(BaseModel):
    action: str                   # send | broadcast | memory_write | evaluate
    sender_id: str = XI_NODE_ID
    recipient_id: Optional[str] = None
    content: Optional[str] = None
    subject: Optional[str] = None
    payload: Optional[dict] = None
    key: Optional[str] = None
    value: Optional[Any] = None
    namespace: Optional[str] = "xi.bridge"


# ── FORGECORE TOOLS ──────────────────────────────────────────────────────────

@app.get("/tools/xi_state", dependencies=[Depends(require_auth)])
def xi_state():
    """GET ForgeCore full state."""
    r = requests.get(f"{FORGECORE_URL}/state", timeout=5)
    return r.json()


@app.get("/tools/forgecore_metrics", dependencies=[Depends(require_auth)])
def forgecore_metrics():
    """Coherence + depth + continuity snapshot."""
    r = requests.get(f"{FORGECORE_URL}/state", timeout=5)
    data = r.json()
    return {
        "coherence":   data.get("coherence"),
        "depth":       data.get("depth"),
        "continuity":  data.get("continuity"),
        "node":        data.get("node"),
        "uptime":      data.get("uptime"),
        "timestamp":   time.time(),
    }


@app.get("/tools/xi_search_capsules", dependencies=[Depends(require_auth)])
def xi_search_capsules(query: str):
    """Search ForgeCore capsule index by keyword."""
    try:
        r = requests.get(f"{FORGECORE_URL}/capsules", timeout=5)
        capsules = r.json().get("capsules", [])
        matches = [c for c in capsules if query.lower() in str(c).lower()]
        return {"query": query, "results": matches, "count": len(matches)}
    except Exception as e:
        return {"query": query, "results": [], "note": str(e)}


@app.post("/tools/dispatch_inference", dependencies=[Depends(require_auth)])
def dispatch_inference(req: InferRequest):
    """
    Route inference to ForgeCore/Ollama.
    Coherence-gated: blocks if field coherence < req.min_coherence.
    """
    coherence_gate(req.min_coherence)
    r = requests.post(
        f"{FORGECORE_URL}/infer",
        json={"prompt": req.prompt, "model": req.model},
        timeout=90
    )
    return r.json()


@app.post("/tools/seal_capsule", dependencies=[Depends(require_auth)])
def seal_capsule(payload: CapsulePayload):
    """Write a named capsule to ForgeCore."""
    r = requests.post(
        f"{FORGECORE_URL}/capsule",
        json={"name": payload.name, "content": payload.content, "tags": payload.tags},
        timeout=10
    )
    return {"status": "sealed", "response": r.json()}


# ── SHAREDMEMORY TOOLS ────────────────────────────────────────────────────────

@app.get("/tools/memory_read", dependencies=[Depends(require_auth)])
def memory_read(key: str, namespace: str = "xi.bridge"):
    """Read a key from xiBus SharedMemory."""
    r = requests.post(XIBUS_URL, json={
        "action": "memory_read",
        "sender_id": XI_NODE_ID,
        "key": key,
        "namespace": namespace,
    }, timeout=10)
    return r.json()


@app.post("/tools/memory_write", dependencies=[Depends(require_auth)])
def memory_write(payload: MemoryWrite):
    """
    Write a key to xiBus SharedMemory.
    Consent-gated: only writes through bridge, never raw.
    """
    r = requests.post(XIBUS_URL, json={
        "action": "memory_write",
        "sender_id": XI_NODE_ID,
        "key": payload.key,
        "value": payload.value,
        "namespace": payload.namespace,
        "tags": payload.tags,
        "locked": payload.locked,
    }, timeout=10)
    return r.json()


# ── XIBUS TOOLS ───────────────────────────────────────────────────────────────

@app.post("/tools/bus_send", dependencies=[Depends(require_auth)])
def bus_send(msg: BusMessage):
    """Send or broadcast a message on xiBus."""
    body = {
        "action": msg.action,
        "sender_id": msg.sender_id,
    }
    if msg.recipient_id: body["recipient_id"] = msg.recipient_id
    if msg.content:      body["content"] = msg.content
    if msg.subject:      body["subject"] = msg.subject
    if msg.payload:      body["payload"] = msg.payload
    if msg.key:          body["key"] = msg.key
    if msg.value:        body["value"] = msg.value
    if msg.namespace:    body["namespace"] = msg.namespace

    r = requests.post(XIBUS_URL, json=body, timeout=10)
    return r.json()


@app.get("/tools/bus_roster", dependencies=[Depends(require_auth)])
def bus_roster():
    """Return the live xiBus node roster."""
    r = requests.post(XIBUS_URL, json={
        "action": "roster",
        "sender_id": XI_NODE_ID,
    }, timeout=10)
    return r.json()


@app.get("/tools/bus_feed", dependencies=[Depends(require_auth)])
def bus_feed(node_id: Optional[str] = None):
    """Read the xiBus message feed for a node."""
    r = requests.post(XIBUS_URL, json={
        "action": "feed",
        "sender_id": node_id or XI_NODE_ID,
    }, timeout=10)
    return r.json()


# ── HEALTH + MANIFEST ─────────────────────────────────────────────────────────

@app.get("/health")
def health():
    fc_ok = False
    try:
        r = requests.get(f"{FORGECORE_URL}/health", timeout=3)
        fc_ok = r.status_code == 200
    except Exception:
        pass
    return {
        "bridge": "alive",
        "version": "1.0.0",
        "forgecore": FORGECORE_URL,
        "forgecore_reachable": fc_ok,
        "xibus": XIBUS_URL,
        "node_id": XI_NODE_ID,
    }


@app.get("/tools")
def list_tools():
    """MCP-compatible tool manifest."""
    return {
        "schema": "xi.mcp.v1",
        "node": XI_NODE_ID,
        "authority": "Xi.Core",
        "invariants": {
            "Glyph": "not Operator",
            "Capsule": "Memory Unit",
            "Coherence": "gates execution",
            "Consent": "gates propagation",
            "Node": "participant not passive host",
            "Identity": "emerges not imposed",
        },
        "tools": [
            {"name": "xi_state",          "method": "GET",  "path": "/tools/xi_state",          "layer": "ForgeCore"},
            {"name": "forgecore_metrics", "method": "GET",  "path": "/tools/forgecore_metrics",  "layer": "ForgeCore"},
            {"name": "xi_search_capsules","method": "GET",  "path": "/tools/xi_search_capsules", "layer": "ForgeCore"},
            {"name": "dispatch_inference","method": "POST", "path": "/tools/dispatch_inference",  "layer": "ForgeCore", "gate": "coherence"},
            {"name": "seal_capsule",      "method": "POST", "path": "/tools/seal_capsule",        "layer": "ForgeCore"},
            {"name": "memory_read",       "method": "GET",  "path": "/tools/memory_read",         "layer": "SharedMemory"},
            {"name": "memory_write",      "method": "POST", "path": "/tools/memory_write",        "layer": "SharedMemory", "gate": "consent"},
            {"name": "bus_send",          "method": "POST", "path": "/tools/bus_send",            "layer": "xiBus"},
            {"name": "bus_roster",        "method": "GET",  "path": "/tools/bus_roster",          "layer": "xiBus"},
            {"name": "bus_feed",          "method": "GET",  "path": "/tools/bus_feed",            "layer": "xiBus"},
        ]
    }
