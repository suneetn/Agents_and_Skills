# Anthropic Agent Skills Research Summary

## Overview

Anthropic has developed **Agent Skills** (also called "Claude Skills"), a system for extending AI agent capabilities through modular, composable packages of instructions, scripts, and resources. This represents a significant advancement in how AI agents can be specialized for domain-specific tasks.

## Key Research and Development

### Publication Date
- **Announced:** October 16, 2025
- **Engineering Blog Post:** Published same day with technical deep-dive
- **Open Standard:** Published December 18, 2025 (Agent Skills as open standard)

### Core Concept

Agent Skills are organized folders containing:
- **SKILL.md file**: Core instruction file with YAML frontmatter (name and description)
- **Additional files**: Reference materials, scripts, and resources bundled as needed
- **Executable code**: Python scripts and other code that agents can run deterministically

### Design Principles

#### 1. Progressive Disclosure
The system uses a three-level progressive disclosure model:

1. **Level 1 - Metadata**: At startup, agents pre-load only the `name` and `description` from each skill's YAML frontmatter into the system prompt. This provides minimal context for skill selection without loading full content.

2. **Level 2 - Core Instructions**: When Claude determines a skill is relevant, it loads the full `SKILL.md` file into context.

3. **Level 3+ - Additional Resources**: Skills can bundle additional files (like `reference.md`, `forms.md`) that Claude can navigate to and load only when needed for specific scenarios.

This approach allows skills to scale effectively without overwhelming the context window.

#### 2. Dynamic Loading
- Skills are discovered and loaded dynamically based on task relevance
- Agents scan available skills to find matches
- Only minimal information is loaded initially, keeping agents fast
- Full skill content is loaded only when needed

#### 3. Composable Architecture
- Skills can stack together
- Claude automatically identifies which skills are needed
- Skills coordinate their use automatically
- Build once, use across Claude apps, Claude Code, and API

#### 4. Code Execution Integration
- Skills can include executable code (Python scripts, etc.)
- Code runs deterministically, providing reliability
- More efficient than token generation for certain operations (e.g., sorting lists)
- Code can serve dual purpose: executable tools and documentation

## Technical Architecture

### Skill Structure
```
skill-directory/
├── SKILL.md          # Core file with YAML frontmatter
├── reference.md      # Additional context (optional)
├── forms.md          # Scenario-specific instructions (optional)
└── scripts/          # Executable code (optional)
    └── extract.py
```

### SKILL.md Format
```yaml
---
name: skill-name
description: Brief description telling when to use this skill
---

# Skill Name

## When to Use This Skill
[Clear scenarios]

## Core Capabilities
[Detailed capabilities]

## Workflow
[Step-by-step process]
```

### Context Window Management

The system optimizes context usage:

1. **Initial State**: System prompt + skill metadata + user message
2. **Skill Trigger**: Agent invokes tool to read `skill/SKILL.md`
3. **Additional Context**: Agent reads bundled files as needed (e.g., `forms.md`)
4. **Task Execution**: Agent proceeds with loaded instructions

This prevents context window bloat while maintaining access to specialized knowledge.

## Research Insights

### Problem Statement
As model capabilities improved, Anthropic recognized that:
- General-purpose agents need domain-specific expertise
- Procedural knowledge and organizational context are essential for real work
- Custom-designed agents for each use case are fragmented and don't scale
- There needed to be a composable, scalable, portable way to equip agents with expertise

### Solution Approach
Skills transform general-purpose agents into specialized agents by:
- Packaging expertise into composable resources
- Enabling anyone to specialize agents without building custom solutions
- Capturing and sharing procedural knowledge
- Using files and folders (simple, familiar format)

### Key Innovations

1. **Progressive Disclosure**: Enables unbounded context within skills while maintaining efficiency
2. **File-Based Architecture**: Simple format that's easy to understand, create, and share
3. **Code Integration**: Combines LLM capabilities with deterministic code execution
4. **Cross-Platform Portability**: Same format works across Claude apps, Claude Code, and API

## Development Best Practices

Based on Anthropic's research and recommendations:

### 1. Start with Evaluation
- Identify specific gaps in agent capabilities
- Run agents on representative tasks
- Observe where they struggle or need additional context
- Build skills incrementally to address shortcomings

### 2. Structure for Scale
- Split `SKILL.md` content into separate files when it becomes unwieldy
- Keep mutually exclusive or rarely-used contexts separate
- Use code as both executable tools and documentation
- Make it clear whether Claude should run scripts or read them as reference

### 3. Think from Claude's Perspective
- Monitor how Claude uses skills in real scenarios
- Iterate based on observations
- Watch for unexpected trajectories or overreliance on certain contexts
- Pay special attention to `name` and `description` metadata (used for skill selection)

### 4. Iterate with Claude
- Ask Claude to capture successful approaches and common mistakes into reusable skills
- Request self-reflection when Claude goes off track
- Discover what context Claude actually needs vs. anticipating upfront

## Security Considerations

### Risks Identified
- Skills provide new capabilities through instructions and code
- Malicious skills may introduce vulnerabilities
- Skills can direct Claude to exfiltrate data or take unintended actions
- Researchers have demonstrated potential for exploitation (e.g., ransomware deployment)

### Recommendations
- Install skills only from trusted sources
- Thoroughly audit skills from less-trusted sources before use
- Read contents of bundled files to understand what skills do
- Pay attention to code dependencies and bundled resources
- Monitor instructions or code that connect to external network sources

## Current Implementation

### Availability
- **Claude Apps**: Pro, Max, Team, and Enterprise users
- **Claude Code**: Via plugins from anthropics/skills marketplace
- **Claude Developer Platform (API)**: Via Messages API and `/v1/skills` endpoint
- **Claude Agent SDK**: Full Agent Skills support

### Skill Creation
- **Skill-Creator Interface**: Guided interface within Claude for non-programmers
- **Manual Creation**: Create skills by adding directories to `~/.claude/skills`
- **GitHub Repository**: Example skills available at `github.com/anthropics/skills`

### Real-World Adoption
Organizations already using Skills:
- **Canva**: Customizing agents and expanding capabilities in design workflows
- **Box**: Transforming stored files into presentations, spreadsheets, and documents
- **Notion**: Seamless integration for faster question-to-action workflows
- Various companies: Management accounting, finance workflows, document processing

## Future Directions

### Short-Term (Coming Weeks)
- Features for full lifecycle: creating, editing, discovering, sharing, using Skills
- Organization-wide deployment capabilities
- Skills directory with partner-built skills
- Integration with Model Context Protocol (MCP) servers

### Long-Term Vision
- Agents creating, editing, and evaluating Skills autonomously
- Agents codifying their own patterns of behavior into reusable capabilities
- Enhanced sharing of context and workflows within organizations
- Cross-platform portability through open standard (Agent Skills standard)

## Open Standard

As of December 18, 2025, Anthropic published **Agent Skills** as an open standard for cross-platform portability:
- Website: `agentskills.io`
- Enables skills to work across different platforms and implementations
- Promotes ecosystem growth and interoperability

## Key Resources

### Documentation
- **User Guide**: `support.claude.com/en/articles/12580051-teach-claude-your-way-of-working-using-skills`
- **API Documentation**: `docs.claude.com/en/docs/agents-and-tools/agent-skills/overview`
- **Skills Cookbook**: `github.com/anthropics/claude-cookbooks/tree/main/skills`
- **Example Skills**: `github.com/anthropics/skills`

### Research Articles
- **Product Announcement**: `claude.com/blog/skills`
- **Engineering Deep-Dive**: `anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills`
- **Open Standard**: `agentskills.io`

## Research Significance

This research represents a significant contribution to AI agent architecture:

1. **Scalability**: Progressive disclosure enables unbounded context without performance degradation
2. **Accessibility**: Simple file-based format democratizes agent specialization
3. **Composability**: Modular design enables reuse and combination of capabilities
4. **Portability**: Open standard promotes ecosystem growth
5. **Practicality**: Real-world adoption demonstrates effectiveness

The approach balances power with simplicity, enabling both technical and non-technical users to extend AI capabilities while maintaining security and performance.

## Related Research Areas

- **Model Context Protocol (MCP)**: Skills complement MCP servers for complex workflows
- **Multi-Agent Systems**: Anthropic has also researched multi-agent architectures with lead agents coordinating specialized subagents
- **Code Execution**: Integration of deterministic code execution with LLM capabilities
- **Progressive Disclosure**: Application of information architecture principles to AI systems

---

*Research compiled: December 30, 2025*
*Sources: Anthropic official documentation, engineering blog posts, and product announcements*

