# Qr Code Ai

> By [MEOK AI Labs](https://meok.ai) — MEOK AI Labs MCP Server

QR Code AI MCP Server — QR code generation and data tools.

## Installation

```bash
pip install qr-code-ai-mcp
```

## Usage

```bash
# Run standalone
python server.py

# Or via MCP
mcp install qr-code-ai-mcp
```

## Tools

### `generate_qr_data`
Generate QR code data from text/URL. Returns matrix or text-art representation.

**Parameters:**
- `content` (str)
- `error_correction` (str)
- `output_format` (str)

### `decode_qr_data`
Analyze a QR matrix (JSON 2D array) and extract metadata.

**Parameters:**
- `matrix_json` (str)

### `create_vcard_qr`
Generate vCard data suitable for QR encoding.

**Parameters:**
- `name` (str)
- `phone` (str)
- `email` (str)
- `org` (str)
- `title` (str)
- `url` (str)

### `create_wifi_qr`
Generate WiFi QR code data for network sharing.

**Parameters:**
- `ssid` (str)
- `password` (str)
- `security` (str)
- `hidden` (bool)


## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## Links

- **Website**: [meok.ai](https://meok.ai)
- **GitHub**: [CSOAI-ORG/qr-code-ai-mcp](https://github.com/CSOAI-ORG/qr-code-ai-mcp)
- **PyPI**: [pypi.org/project/qr-code-ai-mcp](https://pypi.org/project/qr-code-ai-mcp/)

## License

MIT — MEOK AI Labs
