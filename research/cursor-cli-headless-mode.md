# Cursor CLI Headless Mode Research
**Research Date:** January 3, 2025

## Overview
Yes, Cursor offers a Command-Line Interface (CLI) that supports headless operation, enabling non-interactive execution similar to Claude Code. This functionality is particularly useful for integrating Cursor into scripts, automation workflows, and CI/CD pipelines.

---

## Installation

### Install Cursor CLI
```bash
curl https://cursor.com/install -fsS | bash
```

**Note:** Ensure the installation path (typically `~/.local/bin`) is included in your system's `PATH` variable.

### Authentication
Set your API key as an environment variable:
```bash
export CURSOR_API_KEY=your_api_key_here
```

---

## Core Command: `cursor-agent`

The primary command for headless operation is `cursor-agent`.

### Basic Usage

**Non-Interactive Execution (Print Mode)**
```bash
cursor-agent -p "Your command or prompt here"
```

The `-p` (or `--print`) flag enables print mode, allowing non-interactive execution without GUI prompts.

**Example:**
```bash
cursor-agent -p "Analyze this codebase"
cursor-agent -p "Refactor this code to use modern ES6+ syntax"
```

### File Modification

**Propose Changes Only (Default)**
By default, `cursor-agent -p` will propose changes without applying them.

**Apply Changes Directly**
To allow the agent to make direct file modifications without confirmation, combine `--print` with `--force`:
```bash
cursor-agent -p --force "Add JSDoc comments to this file"
```

**Important:** Without `--force`, changes are only proposed, not applied.

---

## Output Formats

### Text Format (Human-Readable)
```bash
cursor-agent -p --output-format text "What does this codebase do?"
```

### JSON Format (Structured)
```bash
cursor-agent -p --output-format json "Analyze this code"
```

---

## Use Cases & Examples

### 1. Code Analysis
```bash
cursor-agent -p --output-format text "What does this codebase do?"
```

### 2. Automated Code Review
```bash
cursor-agent -p --force --output-format text \
  "Review the recent code changes and provide feedback on:
  - Code quality and readability
  - Potential bugs or issues
  - Security considerations
  - Best practices compliance"
```

### 3. Batch Processing Multiple Files
```bash
find src/ -name "*.js" | while read file; do
  cursor-agent -p --force "Add comprehensive JSDoc comments to $file"
done
```

### 4. Code Refactoring
```bash
cursor-agent -p --force "Refactor this code to use modern ES6+ syntax"
```

### 5. Documentation Generation
```bash
cursor-agent -p --force "Add JSDoc comments to this file"
```

---

## Shell Mode

Cursor also supports **Shell Mode**, which enables execution of shell commands directly from the CLI:

- Commands are checked against permissions and team settings
- Safety checks are performed before execution
- Output is displayed in the conversation
- Admin policies may block certain commands
- Commands with redirection cannot be allowlisted inline

---

## Limitations & Considerations

### Timeout Limits
- Commands timeout after **30 seconds**
- Long-running processes are not supported
- Interactive prompts are not supported
- Servers cannot be run through the CLI

### Security Considerations
- The CLI is still in **beta** (as of research date)
- Security safeguards are evolving
- Can read, modify, and delete files
- Can execute shell commands (with approval)
- **Recommendation:** Use in trusted environments and review commands before execution

### Permissions
- Commands are checked against your permissions and team settings
- Admin policies may block certain commands
- Commands with redirection cannot be allowlisted inline

### Known Issues (Resolved)
- **Previous Issue:** Earlier versions had a bug where the CLI wouldn't release the terminal after execution, requiring manual termination
- **Status:** Fixed in version `2025.09.18-7ae6800`
- **Current Status:** Issue has been resolved in recent updates

---

## Comparison with Claude Code

### Similarities
- Both support headless/CLI execution
- Both enable non-interactive scripting and automation
- Both can be integrated into CI/CD pipelines
- Both support batch processing workflows

### Differences
- **Cursor:** Uses `cursor-agent` command with `-p` flag for headless mode
- **Claude Code:** Uses different command structure (specific details would require separate research)
- **Cursor:** Has explicit `--force` flag for file modifications
- **Cursor:** Supports output format options (`text` vs `json`)
- **Cursor:** Has 30-second timeout limitation
- **Cursor:** Includes Shell Mode for direct shell command execution

---

## Integration Examples

### CI/CD Pipeline Integration
```bash
#!/bin/bash
# Example: Automated code review in CI pipeline

echo "Running Cursor code review..."

cursor-agent -p --output-format text \
  "Review the code changes in this commit and identify:
  - Security vulnerabilities
  - Code quality issues
  - Best practices violations"
```

### Script Automation
```bash
#!/bin/bash
# Example: Automated documentation generation

for file in $(find . -name "*.py" -type f); do
  echo "Processing $file..."
  cursor-agent -p --force "Add comprehensive docstrings to $file"
done
```

---

## Best Practices

1. **Use `--force` Carefully:** Only use when you want direct file modifications
2. **Review Output:** Always review proposed changes before applying
3. **Set Timeout Expectations:** Keep commands under 30 seconds
4. **Use Appropriate Output Format:** Use `text` for human reading, `json` for parsing
5. **Secure API Keys:** Store API keys securely, don't commit them to repositories
6. **Test in Safe Environment:** Test scripts in isolated environments first
7. **Check Permissions:** Ensure your team settings allow the commands you need

---

## Documentation References

- **Headless Mode Documentation:** [docs.cursor.com/en/cli/headless](https://docs.cursor.com/en/cli/headless)
- **Shell Mode Documentation:** [docs.cursor.com/en/cli/shell-mode](https://docs.cursor.com/en/cli/shell-mode)
- **CLI Blog Post:** [cursor.com/blog/cli](https://cursor.com/blog/cli)
- **Forum Discussion:** [forum.cursor.com/t/cursor-cli-headless-mode-does-not-release-the-terminal](https://forum.cursor.com/t/cursor-cli-headless-mode-does-not-release-the-terminal/133624)

---

## Summary

**Yes, Cursor has CLI/headless mode** that is similar to Claude Code's capabilities:

✅ **Available Features:**
- Non-interactive execution via `cursor-agent -p`
- Direct file modification with `--force` flag
- Batch processing support
- Multiple output formats (text/json)
- Shell Mode for command execution
- Integration with scripts and CI/CD pipelines

⚠️ **Limitations:**
- 30-second timeout
- No long-running processes
- No interactive prompts
- Still in beta (security evolving)
- Requires API key authentication

🎯 **Best For:**
- Automated code reviews
- Batch refactoring tasks
- Documentation generation
- Code analysis scripts
- CI/CD pipeline integration

---

## Quick Reference

```bash
# Install
curl https://cursor.com/install -fsS | bash

# Authenticate
export CURSOR_API_KEY=your_api_key_here

# Basic usage (propose changes)
cursor-agent -p "Your prompt"

# Apply changes directly
cursor-agent -p --force "Your prompt"

# Text output
cursor-agent -p --output-format text "Your prompt"

# JSON output
cursor-agent -p --output-format json "Your prompt"
```

