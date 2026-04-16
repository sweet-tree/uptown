# MCP setup (Cursor)

This repo includes **[`.cursor/mcp.json`](./mcp.json)** (project-scoped MCP). Cursor reads it when you open the workspace—**fully quit and reopen Cursor** after changing it so the Playwright server starts.

To reuse on **another repo**, copy that JSON into the new project’s `.cursor/mcp.json`, or merge the `playwright` entry into **`~/.cursor/mcp.json`** if you want it in every project.

## Playwright (default)

- **Local dev** (`http://localhost:3000`, etc.) and **public URLs** both work: the server runs on your machine via `npx`.
- Docs: [Playwright MCP](https://playwright.dev/docs/getting-started-mcp)

## Standalone HTTP (SSH / no headed browser in the IDE worker)

```bash
npx -y @playwright/mcp@latest --port 8931
```

Point MCP at `http://localhost:8931/mcp` instead of the `command` block.

## Optional: Puppeteer MCP (screenshots / `evaluate`)

```json
"puppeteer": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
}
```

Use alongside or instead of Playwright depending on RAM; most workflows only need Playwright.
