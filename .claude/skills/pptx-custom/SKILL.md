---
name: pptx-custom
description: "Custom presentation skill for leader-app. Extends the base pptx skill with project-specific preferences for leadership and management presentations."
---

# Custom PowerPoint Skill

This skill customizes PowerPoint generation for leadership/management content.

## When to Use This Skill

Use this skill when creating presentations for:
- Performance reviews and calibration
- Team narratives and status updates  
- Strategy documents and roadmaps
- Leadership training materials

## Design Preferences

### Color Palettes

**Default - Executive Dark:**
- Primary: #1C2833 (deep charcoal)
- Secondary: #2E4053 (slate blue)
- Accent: #E74C3C (strong red)
- Highlight: #F39C12 (amber)
- Light: #F4F6F6 (off-white)

**Alternative - Professional Blue:**
- Primary: #2C3E50
- Secondary: #3498DB
- Accent: #E67E22
- Light: #ECF0F1

### Typography
- Headers: Arial Bold
- Body: Arial Regular
- Quotes: Georgia Italic
- All fonts must be web-safe

### Layout Conventions
- 16:9 aspect ratio (720pt × 405pt)
- Header bars at top of content slides
- Color-coded section dividers
- Consistent margin: 0.5 inches

## Content Structure

For leadership presentations, follow this structure:
1. **Title slide** - Topic + key metrics/context
2. **Frame/Context** - Why this matters
3. **Agenda/Overview** - What we'll cover
4. **Content sections** - One topic per slide
5. **Summary/Checklist** - Key takeaways
6. **Closing** - Call to action or next steps

## Scripts Location

Base scripts are at: `~/.claude/skills/pptx/scripts/`
- html2pptx.js - HTML to PowerPoint conversion
- thumbnail.py - Generate slide previews
- inventory.py - Extract text from templates

## Customization Notes

Add your customizations below this line:
---

<!-- Your custom instructions here -->
