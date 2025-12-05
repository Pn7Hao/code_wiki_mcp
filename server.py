from mcp.server.fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup
import re

# Initialize FastMCP server
mcp = FastMCP("CodeWiki")

@mcp.tool()
def search_code_wiki(repo_url: str, query: str = "") -> str:
    """
    Retrieves information about a repository from Google CodeWiki.
    
    Args:
        repo_url: The full URL of the repository (e.g., https://github.com/microsoft/vscode-copilot-chat)
        query: Specific topic or question to search for within the page content (optional).
    """
    # Clean repo URL to match CodeWiki format
    # Format appears to be: https://codewiki.google/domain/owner/repo
    # Example: https://codewiki.google/github.com/microsoft/vscode-copilot-chat
    
    clean_repo = repo_url.replace("https://", "").replace("http://", "")
    target_url = f"https://codewiki.google/{clean_repo}"
    
    try:
        # Note: This relies on the environment having network access to codewiki.google
        headers = {
            "User-Agent": "MCP-Agent/1.0"
        }
        response = requests.get(target_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find the main content. This is heuristic since we don't know the exact DOM.
        # We'll grab body text.
        for script in soup(["script", "style"]):
            script.decompose()
            
        text = soup.get_text(separator='\n', strip=True)
        
        # Simple content filtering if query is provided
        if query:
            # simple keyword matching
            lines = text.split('\n')
            relevant_lines = [line for line in lines if query.lower() in line.lower()]
            if relevant_lines:
                return f"Found relevant sections for '{query}' in {target_url}:\n\n" + "\n".join(relevant_lines[:20]) # Limit output
            else:
                return f"Could not find specific mentions of '{query}' in the page. Here is the beginning of the page:\n\n{text[:1000]}"
        
        return f"Content from {target_url}:\n\n{text[:2000]}..." # Truncate to avoid huge context
        
    except requests.exceptions.RequestException as e:
        return f"Error accessing CodeWiki ({target_url}). Please ensure you have access to this internal URL.\nError: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    mcp.run()
