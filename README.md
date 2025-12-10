# CodeWiki MCP Server

MCP server that drives the Google CodeWiki web UI (via Selenium) to answer questions about GitHub repositories.

## Prerequisites

- Python 3.10+
- Google Chrome and a compatible ChromeDriver available on `PATH`
- Dependencies: `mcp`, `selenium`

## Installation

```bash
# Using uv (recommended)
uv pip install mcp selenium

# Or using pip
pip install mcp selenium
```

## Configuration

Example VS Code MCP config (`.vscode/mcp.json`) for the included virtualenv:

```json
{
  "servers": {
    "codewiki": {
      "command": "c:\\Users\\haopn2\\Documents\\code_wiki_mcp\\venv\\Scripts\\python.exe",
      "args": [
        "c:\\Users\\haopn2\\Documents\\code_wiki_mcp\\server.py",
        "--transport",
        "streamable-http",
        "--host",
        "127.0.0.1",
        "--port",
        "18080",
        "--disable-dns-rebinding"
      ]
    }
  }
}
```

### Exposing over HTTPS / tunnels (GitHub Copilot Agents)

FastMCP enables DNS rebinding protection by default, which rejects requests whose `Host`/`Origin` headers do not match `127.0.0.1`. When you front this server with an HTTPS tunnel or proxy (Cloudflare Tunnel, ngrok, etc.), you must relax those checks:

- Recommended: explicitly allow your public host/origin

  ```bash
  python server.py --transport streamable-http --host 127.0.0.1 --port 18080 \
    --allow-host my-public-domain:* \
    --allow-origin https://my-public-domain
  ```

- Alternative (less strict, but convenient for ad-hoc tunnels): `--disable-dns-rebinding`

  ```bash
  python server.py --transport streamable-http --host 127.0.0.1 --port 18080 --disable-dns-rebinding
  ```

The sample `.vscode/mcp.json` above uses the safe-but-flexible `--disable-dns-rebinding` flag so GitHub Copilot Agents can reach the server through an HTTPS endpoint.

## Tools

### `search_code_wiki`

Ask the CodeWiki chat UI about a repository.

- `repo_url`: Full repository URL (e.g., `https://github.com/microsoft/vscode-copilot-chat`)
- `query`: Required question for CodeWiki (e.g., `Where are the Allow/Skip buttons implemented?`)
