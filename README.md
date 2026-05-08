<div align="center">

# Qr Code Ai MCP

**QR Code AI MCP Server — QR code generation and data tools.**

[![PyPI](https://img.shields.io/pypi/v/meok-qr-code-ai-mcp)](https://pypi.org/project/meok-qr-code-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

QR Code AI MCP Server — QR code generation and data tools.

## Tools

| Tool | Description |
|------|-------------|
| `generate_qr_data` | Generate QR code data from text/URL. Returns matrix or text-art representation. |
| `decode_qr_data` | Analyze a QR matrix (JSON 2D array) and extract metadata. |
| `create_vcard_qr` | Generate vCard data suitable for QR encoding. |
| `create_wifi_qr` | Generate WiFi QR code data for network sharing. |

## Installation

```bash
pip install meok-qr-code-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "qr-code-ai": {
      "command": "python",
      "args": ["-m", "meok_qr_code_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 4 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
