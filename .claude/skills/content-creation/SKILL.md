---
name: content-creation
description: Use this skill when the user wants to create content from ideation to final draft. This skill automatically orchestrates the complete workflow: brainstorming topics (using content-ideation), researching information (using researcher), structuring content, writing in personal voice (using writing-content-in-personal-voice), and refining the output. The user invokes this skill once and it handles all phases automatically. Trigger keywords: "create content", "write from scratch", "ideation to publication", "full content workflow", "create content from scratch".
---

# Content Creation Workflow

Orchestrate the complete content creation process from ideation through research, writing, and refinement. **This skill automatically coordinates all phases** - you invoke it once and it handles ideation, research, writing, and refinement automatically by calling the appropriate skills.

## How to Use

**Simple Usage (Recommended):**
Just invoke this skill with your content request:
- "Create a LinkedIn post from scratch about AI implementation"
- "Write an article from ideation to publication on document intelligence"

The skill will automatically:
1. Generate ideas using `content-ideation` skill
2. Research using `researcher` skill  
3. Write using `writing-content-in-personal-voice` skill
4. Refine and optimize the final content

**Advanced Usage (More Control):**
You can also invoke individual skills separately if you want more control:
- Use `content-ideation` first to brainstorm
- Then use `researcher` to gather information
- Then invoke this workflow skill with your selected topic

## Core Approach

**This skill automatically orchestrates all phases.** When invoked, it:

1. **Ideate** - Automatically calls `content-ideation` skill to generate topic ideas and angles
2. **Research** - Automatically calls `researcher` skill to gather supporting information
3. **Structure** - Organizes content outline and framework based on ideation and research
4. **Write** - Automatically calls `writing-content-in-personal-voice` skill to create content
5. **Refine** - Reviews, edits, and optimizes the final content

**You don't need to manually invoke each skill** - this workflow skill handles all coordination automatically.

See `./reference/workflow-steps.md` for detailed step-by-step guidance and `./reference/integration-patterns.md` for how skills work together.

## Step-by-Step Instructions

### 1. Ideation Phase

**Use `content-ideation` skill to generate ideas:**

1. **Understand requirements:**
   - What type of content? (LinkedIn post, article, framework)
   - What's the goal? (Educate, engage, convert)
   - Who's the audience?
   - Any constraints or starting points?

2. **Generate ideas:**
   - Brainstorm multiple angles and hooks
   - Explore contrarian, research, framework, and problem-solution angles
   - Develop compelling hooks and titles
   - See `~/.claude/skills/content-ideation/SKILL.md` for ideation methods

3. **Evaluate and select:**
   - Assess potential, uniqueness, and feasibility
   - Prioritize top ideas
   - Select final topic/angle for development

**Output**: Selected topic with hook, angle, key points, and format recommendation

### 2. Research Phase

**Use `researcher` skill to gather information:**

1. **Define research needs:**
   - What information is needed to support the content?
   - What data or evidence would strengthen the piece?
   - Are there examples or case studies to include?

2. **Conduct research:**
   - Use `researcher` skill for multi-source research
   - Gather data, statistics, examples
   - Find supporting evidence and case studies
   - See `~/.claude/skills/researcher/SKILL.md` for research methods

3. **Synthesize findings:**
   - Organize research into key insights
   - Identify data points to include
   - Note sources for credibility
   - Extract actionable takeaways

**Output**: Research findings, key insights, supporting data, and examples

### 3. Structure Phase

**Organize content before writing:**

1. **Create outline:**
   - Define structure based on format (post, article, framework)
   - Map key points to sections
   - Identify where research fits
   - Plan hook, body, and conclusion

2. **Develop framework (if applicable):**
   - Break solution into 3-7 clear steps
   - Define each step with context
   - Plan examples and applications
   - Structure for scannability

3. **Plan implementation:**
   - How will readers apply this?
   - What are the key takeaways?
   - What's the call to action?

**Output**: Content outline, framework structure (if applicable), and key sections

### 4. Writing Phase

**Use `writing-content-in-personal-voice` skill to create content:**

1. **Apply voice principles:**
   - Structured brevity for format
   - Research-informed insights
   - Actionable frameworks
   - Authentic expertise
   - Contrarian clarity when appropriate

2. **Write content:**
   - Follow content structure from outline
   - Use language patterns from personal voice
   - Incorporate research findings naturally
   - Apply formatting guidelines
   - See `~/.claude/skills/writing-content-in-personal-voice/SKILL.md` for writing guidance

3. **Ensure quality:**
   - Check length matches format guidelines
   - Verify research-backed claims have evidence
   - Confirm frameworks are actionable
   - Validate tone and voice consistency

**Output**: Complete draft in personal voice

### 5. Refinement Phase

**Review and optimize content:**

1. **Content review:**
   - Does it achieve the goal?
   - Is the message clear?
   - Are frameworks actionable?
   - Is research integrated well?

2. **Voice check:**
   - Matches personal voice principles?
   - Appropriate tone and style?
   - No corporate speak or jargon?
   - Authentic and honest?

3. **Format optimization:**
   - Length appropriate for format?
   - Formatting follows guidelines?
   - Scannable and readable?
   - Engagement elements included?

4. **Final polish:**
   - Remove unnecessary words
   - Strengthen hooks and openings
   - Clarify key points
   - Add engagement questions if appropriate

5. **Save content (REQUIRED):**
   - **MUST create and write file to `~/personal/content/` directory structure**
   - Determine content type and create appropriate folder:
     - LinkedIn posts: `~/personal/content/linkedin-posts/[topic-name]/`
     - Articles: `~/personal/content/articles/[topic-name]/`
     - Frameworks: `~/personal/content/frameworks/[framework-name]/`
   - Use descriptive, lowercase folder names with hyphens (e.g., `ai-use-cases-2025`)
   - Create markdown file with descriptive name (e.g., `linkedin-post-ai-use-cases-2025.md`)
   - Write file with YAML frontmatter:
     ```yaml
     ---
     title: [Content Title]
     format: [LinkedIn Post/Article/Framework]
     date: [YYYY-MM-DD]
     topic: [Topic tags]
     word_count: [number]
     status: ready
     ---
     ```
   - Write complete final content after frontmatter
   - Use `write` tool to create the file at the determined path
   - Verify file was created successfully

**Output**: Final polished content ready for publication, saved to `~/personal/content/[format]/[topic-name]/[filename].md`

## Workflow Integration

### Skill Coordination

**Ideation → Research → Writing:**

```
1. content-ideation → Generate topic ideas
2. researcher → Gather supporting information
3. writing-content-in-personal-voice → Create content
4. Manual refinement → Review and optimize
```

**When to use each skill:**

- **content-ideation**: When starting from scratch or need fresh ideas
- **researcher**: When information or data is needed
- **writing-content-in-personal-voice**: When ready to write the content
- **content-creation**: When orchestrating the full workflow

See `./reference/integration-patterns.md` for detailed skill coordination patterns.

## Examples

### Example 1: LinkedIn Post Workflow

**User Query**: "I want to create a LinkedIn post about AI implementation from scratch"

**Workflow**:

**Step 1: Ideation**
- Use `content-ideation` to brainstorm angles
- Select: "Focus on one use case" contrarian angle
- Hook: "Most teams are asking AI to do too much..."

**Step 2: Research**
- Use `researcher` to find AI implementation statistics
- Gather: Data on successful vs. failed implementations
- Insight: Teams that start narrow succeed more

**Step 3: Structure**
- Format: LinkedIn post (80-100 words)
- Structure: Hook → Insight → Framework → Question
- Key points: One use case, nail it, then expand

**Step 4: Writing**
- Use `writing-content-in-personal-voice` to write
- Apply structured brevity principles
- Include research-backed insight
- End with engagement question

**Step 5: Refinement**
- Check length (80 words ✓)
- Verify voice consistency
- Ensure scannability
- Final polish

**Output**: Complete LinkedIn post ready to publish

### Example 2: Article Workflow

**User Query**: "Create an article about document intelligence frameworks"

**Workflow**:

**Step 1: Ideation**
- Use `content-ideation` to explore angles
- Select: "4-step framework" approach
- Title: "The 4-Step Framework for Implementing Document Intelligence"

**Step 2: Research**
- Use `researcher` to gather case studies
- Research: Document search solutions and implementations
- Findings: Common failures, successful patterns

**Step 3: Structure**
- Format: Medium article (400-600 words)
- Structure: Problem → Research → Framework → Implementation
- Framework: 4 steps with context and examples

**Step 4: Writing**
- Use `writing-content-in-personal-voice` to write
- Apply framework structure
- Incorporate research findings
- Include actionable steps

**Step 5: Refinement**
- Review completeness
- Verify framework clarity
- Check research integration
- Optimize for readability

**Output**: Complete article ready for publication

## Reference Files

- `./reference/workflow-steps.md` - Detailed step-by-step guidance
- `./reference/integration-patterns.md` - How skills coordinate together
- `./reference/quality-checklist.md` - Content quality validation
- `./templates/workflow-template.md` - Template for tracking workflow progress
- `./templates/content-outline-template.md` - Template for structuring content

## Validation Checklist

Before completing workflow, verify:
- [ ] Topic selected and validated
- [ ] Research completed and synthesized
- [ ] Content structured appropriately
- [ ] Content written in personal voice
- [ ] Length matches format guidelines
- [ ] Research integrated naturally
- [ ] Frameworks are actionable
- [ ] Voice consistency maintained
- [ ] Content refined and polished
- [ ] Ready for publication

## Troubleshooting

### Issue: Workflow feels disconnected

**Solution**:
- Ensure each phase builds on previous phase
- Use outputs from one phase as inputs to next
- Reference `./reference/integration-patterns.md` for coordination
- Maintain context throughout workflow

### Issue: Content doesn't match voice

**Solution**:
- Review voice principles before writing phase
- Use `writing-content-in-personal-voice` skill properly
- Check against voice guidelines during refinement
- Ensure research supports voice (not replaces it)

### Issue: Research overwhelms content

**Solution**:
- Synthesize research into key insights
- Use research to support points, not replace them
- Integrate research naturally into narrative
- Focus on actionable takeaways, not just data

---

Remember: This workflow orchestrates multiple skills to create complete, high-quality content. Each phase builds on the previous, resulting in content that's well-researched, properly structured, and written in your authentic voice.

