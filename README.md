# qr-code-ai-mcp

MCP server for QR code generation and data tools.

## Tools

- **generate_qr_data** — Generate QR code matrix or text-art from content
- **decode_qr_data** — Analyze QR matrix metadata
- **create_vcard_qr** — Generate vCard QR data for contacts
- **create_wifi_qr** — Generate WiFi QR data for network sharing

## Usage

```bash
pip install mcp
python server.py
```

## Rate Limits

50 calls/day per tool (free tier).
