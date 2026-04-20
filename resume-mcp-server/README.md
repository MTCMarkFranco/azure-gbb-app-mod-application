# 📄 Mark Franco — Resume MCP Server

An **interactive resume** built as an MCP (Model Context Protocol) server.
Recruiters and hiring managers can explore Mark Franco's qualifications
conversationally using GitHub Copilot, Claude Desktop, or any MCP-compatible
client.

> **Role target:** Azure GBB Modernization Solution Engineer (Job ID: 200030741)

---

## ✨ What Can You Ask?

| Capability | Description |
|-----------|-------------|
| `resume://summary` | Professional summary |
| `resume://experience` | 19 years at Microsoft |
| `resume://skills` | Technical skills matrix |
| `resume://certifications` | Certifications list |
| `resume://education` | Education background |
| `resume://publications` | Published articles on Medium |
| `search_qualifications(query)` | Full-text search across all sections |
| `match_job_requirements(req)` | Evidence matching for a specific requirement |
| `get_highlights()` | Top 5 most impressive facts |
| `why_hire_mark()` | The compelling case (Easter egg 🥚) |
| `compare_to_role()` | Side-by-side comparison to the Azure GBB Modernization role |
| `interview_mark` | Prompt: mock interview simulation |
| `qualification_deep_dive` | Prompt: deep-dive into a skill area |

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
cd resume-mcp-server
pip install -r requirements.txt
```

### 2. Run the server

```bash
# Standard
python server.py

# Or via the MCP CLI
mcp run server.py
```

The server communicates over **stdio** — it's designed to be launched by an
MCP client, not accessed directly via HTTP.

---

## 🔌 Connect to an MCP Client

### GitHub Copilot (VS Code)

Add to your `.vscode/mcp.json` or workspace settings:

```json
{
  "servers": {
    "mark-franco-resume": {
      "command": "python",
      "args": ["C:\\Projects\\azure-gbb-app-mod-application\\resume-mcp-server\\server.py"]
    }
  }
}
```

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mark-franco-resume": {
      "command": "python",
      "args": ["C:\\Projects\\azure-gbb-app-mod-application\\resume-mcp-server\\server.py"]
    }
  }
}
```

### GitHub Copilot CLI

Add to your `mcp.json`:

```json
{
  "mcpServers": {
    "mark-franco-resume": {
      "command": "python",
      "args": ["C:\\Projects\\azure-gbb-app-mod-application\\resume-mcp-server\\server.py"]
    }
  }
}
```

---

## 💬 Example Conversations

**Recruiter:** "Does Mark have experience with AI?"
→ Copilot calls `search_qualifications("AI")` and returns matches across
  Azure AI Foundry, OpenAI, agentic AI projects, and speaking engagements.

**Hiring Manager:** "How does he compare to our job requirements?"
→ Copilot calls `compare_to_role()` and shows a detailed requirement-by-
  requirement comparison with years of experience and evidence.

**Interviewer:** "Run a mock interview"
→ Copilot uses the `interview_mark` prompt to simulate a structured
  final-round interview with probing follow-ups.

**Anyone:** "Why should we hire Mark?"
→ Copilot calls `why_hire_mark()` and returns a strategic + human argument
  that demonstrates exactly the kind of initiative this role demands.

---

## 🏗️ Architecture

```
┌────────────────────┐     stdio     ┌──────────────────────┐
│  MCP Client        │◄────────────►│  resume-mcp-server   │
│  (Copilot / Claude)│               │  FastMCP (Python)    │
└────────────────────┘               └──────────────────────┘
                                        │
                                        ├── 6 Resources (resume data)
                                        ├── 5 Tools (search, match, compare)
                                        └── 2 Prompts (interview, deep-dive)
```

---

## 📝 License

This project is a personal application artifact.
© 2025 Mark Franco. All rights reserved.
