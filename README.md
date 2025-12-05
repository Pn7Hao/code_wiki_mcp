# CodeWiki MCP Server

This is a Model Context Protocol (MCP) server that provides access to Google's CodeWiki information for open source repositories.

## Prerequisites

- Python 3.10+
- `mcp` library
- `requests`
- `beautifulsoup4`

## Installation

Dependencies are managed via `pip`. Ensure you have the virtual environment set up:

```bash
python -m venv venv
.\venv\Scripts\pip install mcp requests beautifulsoup4
```

## Configuration

To use this server with an MCP client (like Claude Desktop or an IDE), add the following configuration to your MCP settings file:

```json
{
  "mcpServers": {
    "codewiki": {
      "command": "C:\\Users\\haopn2\\Documents\\code_wiki_mcp\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\haopn2\\Documents\\code_wiki_mcp\\server.py"
      ]
    }
  }
}
```

## Tools

### `search_code_wiki`

Retrieves information about a repository from Google CodeWiki.

- `repo_url`: The full URL of the repository (e.g., `https://github.com/microsoft/vscode-copilot-chat`)
- `query`: (Optional) Specific topic or question to search for within the page content.
"# code_wiki_mcp" 
