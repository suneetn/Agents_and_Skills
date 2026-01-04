# Cursor IDE Latest Features Research
**Research Date:** January 3, 2025

## Overview
Cursor has introduced significant updates across multiple versions, with major releases in versions 2.0, 2.2, and 2.3. The focus has been on performance, multi-agent capabilities, integrated development tools, and enhanced user experience.

---

## Major Version Updates

### Version 2.3 (December 22, 2025)

**Stability Improvements**
- Bug fixes and overall stability enhancements
- Improvements to core agent functionality
- Enhanced layout controls
- Better code diff viewing experience

**Layout Customization**
- Four default layouts introduced:
  - **Agent layout**: Optimized for agent interactions
  - **Editor layout**: Traditional coding focus
  - **Zen layout**: Minimal distraction mode
  - **Browser layout**: Integrated browser workflow
- Keyboard shortcuts for quick layout switching
- Personalized workspace configuration

---

### Version 2.2 (December 10, 2025)

**Debug Mode**
- Instruments applications with runtime logs
- Helps reproduce and fix complex bugs
- Compatible across various stacks, languages, and models
- Comprehensive debugging tool within Cursor environment

**Browser Layout and Style Editor**
- Browser sidebar and component tree
- Simultaneous design and coding
- Real-time updates to elements, colors, and layouts
- Changes instantly applied to codebase
- Select elements and forward DOM information to agents

**Plan Mode Enhancements**
- Inline Mermaid diagram support
- Automatic visual generation in plans
- More control over plan execution
- Option to send selected tasks to new agents

**Multi-Agent Judging**
- When running multiple agents in parallel, Cursor evaluates all runs
- Recommends the best solution automatically
- Helps identify optimal approaches

---

### Version 2.0 (October 29, 2025) - Major Release

#### Core Features

**1. Composer: High-Speed Coding Model**
- Cursor's proprietary agentic coding model
- **4x faster** than comparable models
- Completes most tasks in under 30 seconds
- Optimized for incremental diffs across large repositories
- Adaptive reasoning for complex problems
- Supports parallel editing of multiple files

**2. Multi-Agent Parallelism**
- Run up to **8 agents concurrently** on a single prompt
- Each agent operates in isolated copy of codebase
- Uses git worktrees or remote machines to prevent conflicts
- Efficient parallel processing without interference
- Compare different solutions side-by-side

**3. Integrated Browser (General Availability)**
- Transitioned from beta to GA
- Design and code simultaneously within editor
- Tools to select elements and forward DOM information
- Real-time layout and style editing
- Streamlined web development workflow

**4. Voice Mode**
- Speech-to-text conversion for agent control
- Custom submit keywords to trigger actions
- Hands-free interaction with agents
- Natural and efficient workflow

**5. Debug Mode**
- Instruments applications with runtime logs
- Works across various stacks, languages, and models
- Comprehensive debugging within Cursor

**6. Plan Mode Improvements**
- Inline Mermaid diagram support
- Automatic visual generation and streaming
- Create plans with one model, build with another
- Options to build in foreground or background
- Use parallel agents for multiple plans

**7. Sandboxed Terminals (General Availability)**
- Default on macOS
- Secure sandbox with read/write access to workspace
- No internet access for enhanced security
- Pre-approved commands bypass sandbox

**8. Team Commands**
- Define custom commands and rules for teams
- Centrally managed by team admins
- Automatically applied to all team members
- Shareable via deep links in Cursor Docs

**9. Improved Code Review**
- View all changes from agents across multiple files
- No need to switch between individual files
- Simplified review process

**10. Improved Prompt UI**
- Files and directories displayed inline as pills
- Enhanced copy/pasting prompts with tagged context
- Agents can self-gather context without manual attachment

**11. Improved Agent Harness**
- Enhanced underlying harness for working with agents
- Quality improvements across all models
- Especially improved for GPT-5 Codex

**12. Cloud Agents**
- 99.9% reliability
- Instant startup
- Improved UI
- Enhanced experience for sending agents to cloud from editor

**13. Cursor for Enterprise**
- Admin controls for sandboxed terminals
- Hooks for cloud distribution
- Audit log for tracking admin events

**14. Performance Improvements**
- Faster loading and usage of Language Server Protocols (LSPs)
- Improvements across all languages
- Notable improvements in Python and TypeScript LSPs for large projects
- Optimized memory usage
- Fixed several memory leaks
- More stable and responsive development environment

---

## Key Capabilities Summary

### Speed & Performance
- Composer model: 4x faster than comparable models
- Tasks complete in under 30 seconds
- Faster LSP loading across all languages
- Optimized memory usage

### Multi-Agent Capabilities
- Up to 8 parallel agents
- Isolated codebase copies (git worktrees/remote machines)
- Multi-agent judging for best solution recommendation
- No file conflicts between agents

### Integrated Development Tools
- Built-in browser (GA)
- Debug mode with runtime logs
- Plan mode with Mermaid diagrams
- Sandboxed terminals (macOS default)

### User Experience
- Voice mode for hands-free interaction
- Four customizable layouts
- Improved prompt UI with context pills
- Enhanced code review interface

### Team & Enterprise Features
- Team commands and rules
- Shareable commands via deep links
- Enterprise admin controls
- Audit logging

---

## Use Cases Enabled

1. **Parallel Development**: Run multiple agents simultaneously to explore different solutions
2. **Visual Planning**: Generate Mermaid diagrams automatically in plans
3. **Real-time Web Development**: Design and code simultaneously with integrated browser
4. **Voice-Driven Workflow**: Control agents hands-free with voice commands
5. **Secure Execution**: Sandboxed terminals for safe command execution
6. **Team Collaboration**: Shared commands and rules across team members
7. **Fast Iteration**: Composer model enables rapid task completion

---

## Sources
- [Cursor Changelog 2.0](https://cursor.com/changelog/2-0)
- [Cursor Changelog 2.2](https://cursor.com/en/changelog)
- [Cursor Changelog 2.3](https://cursor.com/changelog/)
- [Cursor Forum - Version 2.3](https://forum.cursor.com/t/cursor-2-3-is-here/147076)

---

## Notes
- Most recent version as of research date: 2.3 (December 22, 2025)
- Major focus areas: Performance, multi-agent capabilities, integrated tools, security
- Enterprise features indicate strong focus on team and organizational use cases
- Browser integration suggests emphasis on full-stack web development workflows



