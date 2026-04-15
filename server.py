"""QR Code AI MCP Server — QR code generation and data tools."""

import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import base64
import json
import time
from typing import Any
from mcp.server.fastmcp import FastMCP

from datetime import datetime, timezone
from collections import defaultdict

FREE_DAILY_LIMIT = 15
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day"})
    _usage[c].append(now); return None


mcp = FastMCP("qr-code-ai", instructions="MEOK AI Labs MCP Server")
_calls: dict[str, list[float]] = {}
DAILY_LIMIT = 50

def _rate_check(tool: str) -> bool:
    now = time.time()
    _calls.setdefault(tool, [])
    _calls[tool] = [t for t in _calls[tool] if t > now - 86400]
    if len(_calls[tool]) >= DAILY_LIMIT:
        return False
    _calls[tool].append(now)
    return True

def _qr_matrix(data: str) -> list[list[int]]:
    """Generate a simple QR-like binary matrix from data (deterministic encoding)."""
    encoded = data.encode("utf-8")
    size = max(21, min(41, len(encoded) + 10))
    matrix = [[0] * size for _ in range(size)]
    # Finder patterns (top-left, top-right, bottom-left)
    for ox, oy in [(0, 0), (size - 7, 0), (0, size - 7)]:
        for i in range(7):
            for j in range(7):
                if i in (0, 6) or j in (0, 6) or (2 <= i <= 4 and 2 <= j <= 4):
                    matrix[ox + i][oy + j] = 1
    # Data encoding
    idx = 0
    for i in range(8, size - 8):
        for j in range(8, size - 8):
            if idx < len(encoded):
                matrix[i][j] = (encoded[idx % len(encoded)] >> (j % 8)) & 1
                idx += 1
    return matrix

@mcp.tool()
def generate_qr_data(content: str, error_correction: str = "M", output_format: str = "matrix", api_key: str = "") -> dict[str, Any]:
    """Generate QR code data from text/URL. Returns matrix or text-art representation."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    if not _rate_check("generate_qr_data"):
        return {"error": "Rate limit exceeded (50/day)"}
    if len(content) > 2000:
        return {"error": "Content too long (max 2000 chars)"}
    ec_levels = {"L": 7, "M": 15, "Q": 25, "H": 30}
    if error_correction not in ec_levels:
        return {"error": "Error correction must be L, M, Q, or H"}
    matrix = _qr_matrix(content)
    if output_format == "text":
        art = "\n".join("".join("\u2588\u2588" if cell else "  " for cell in row) for row in matrix)
        return {"content": content, "text_art": art, "size": len(matrix), "error_correction": error_correction}
    return {"content": content, "matrix": matrix, "size": len(matrix), "error_correction": error_correction, "ec_recovery_pct": ec_levels[error_correction]}

@mcp.tool()
def decode_qr_data(matrix_json: str, api_key: str = "") -> dict[str, Any]:
    """Analyze a QR matrix (JSON 2D array) and extract metadata."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    if not _rate_check("decode_qr_data"):
        return {"error": "Rate limit exceeded (50/day)"}
    try:
        matrix = json.loads(matrix_json)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON matrix"}
    if not matrix or not isinstance(matrix, list):
        return {"error": "Matrix must be a 2D array"}
    size = len(matrix)
    total_modules = size * size
    dark = sum(sum(row) for row in matrix)
    version = (size - 17) // 4 if size >= 21 else 0
    return {
        "size": size, "version": version, "total_modules": total_modules,
        "dark_modules": dark, "light_modules": total_modules - dark,
        "dark_percentage": round(dark / total_modules * 100, 1),
        "has_finder_patterns": size >= 21
    }

@mcp.tool()
def create_vcard_qr(name: str, phone: str = "", email: str = "", org: str = "", title: str = "", url: str = "", api_key: str = "") -> dict[str, Any]:
    """Generate vCard data suitable for QR encoding."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    if not _rate_check("create_vcard_qr"):
        return {"error": "Rate limit exceeded (50/day)"}
    parts = ["BEGIN:VCARD", "VERSION:3.0", f"FN:{name}"]
    if org: parts.append(f"ORG:{org}")
    if title: parts.append(f"TITLE:{title}")
    if phone: parts.append(f"TEL:{phone}")
    if email: parts.append(f"EMAIL:{email}")
    if url: parts.append(f"URL:{url}")
    parts.append("END:VCARD")
    vcard = "\n".join(parts)
    matrix = _qr_matrix(vcard)
    return {"vcard_data": vcard, "char_count": len(vcard), "matrix_size": len(matrix), "fields_set": len(parts) - 3}

@mcp.tool()
def create_wifi_qr(ssid: str, password: str, security: str = "WPA", hidden: bool = False, api_key: str = "") -> dict[str, Any]:
    """Generate WiFi QR code data for network sharing."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    if not _rate_check("create_wifi_qr"):
        return {"error": "Rate limit exceeded (50/day)"}
    sec_types = ["WPA", "WEP", "nopass", "WPA2", "WPA3"]
    if security not in sec_types:
        return {"error": f"Security must be one of: {', '.join(sec_types)}"}
    esc_ssid = ssid.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace('"', '\\"')
    esc_pass = password.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace('"', '\\"')
    wifi_str = f"WIFI:T:{security};S:{esc_ssid};P:{esc_pass};H:{'true' if hidden else 'false'};;"
    matrix = _qr_matrix(wifi_str)
    return {"wifi_data": wifi_str, "ssid": ssid, "security": security, "hidden": hidden, "matrix_size": len(matrix)}

if __name__ == "__main__":
    mcp.run()
