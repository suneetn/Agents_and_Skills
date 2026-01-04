---
name: pptx-intuit
description: "Create professional PowerPoint presentations following Intuit brand guidelines. Uses Super Blue (#236CFF), Avenir Next typography, and official color palette from visual.intuit.com"
---

# Intuit PowerPoint Skill

Create professional presentations that follow Intuit's official brand guidelines from [visual.intuit.com](https://visual.intuit.com).

## When to Use This Skill

Use this skill when creating:
- Internal Intuit presentations
- Leadership and team updates
- Strategy documents and roadmaps
- Performance reviews and calibrations
- Training materials
- Product and design reviews

## Brand Overview

**Mission:** Power prosperity around the world  
**Products:** TurboTax, Credit Karma, QuickBooks, Mailchimp

## Color Palette

### Primary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Super Blue** | `#236CFF` | 35, 108, 255 | Primary brand color, CTAs, headers |
| **Midnight** | `#0D2644` | 13, 38, 68 | Dark backgrounds, text |
| **Navy** | `#1A3D5C` | 26, 61, 92 | Secondary dark, accents |
| **Black** | `#000000` | 0, 0, 0 | Text, high contrast |
| **White** | `#FFFFFF` | 255, 255, 255 | Backgrounds, reversed text |

### Light Blues (Super Blue Tints)

| Name | Hex | Usage |
|------|-----|-------|
| **Sky Blue** | `#5A94FF` | Hover states, lighter accents |
| **Light Blue** | `#8FB8FF` | Backgrounds, highlights |
| **Ice Blue** | `#C4DBFF` | Subtle backgrounds |
| **Pale Blue** | `#E8F1FF` | Light backgrounds |

### Secondary "Electric" Colors

| Name | Hex | Usage |
|------|-----|-------|
| **Burgundy** | `#5C1F35` | Deep accent, contrast |
| **Coral** | `#FF6B6B` | Alerts, highlights |
| **Pink** | `#FFB4C4` | Soft accents |
| **Amber** | `#F5A623` | Warnings, attention |
| **Gold** | `#FFCC4D` | Success, positive |
| **Cream** | `#FFF4D9` | Warm backgrounds |
| **Forest Green** | `#0A5C36` | Growth, success |
| **Green** | `#2ECC71` | Positive indicators |
| **Mint** | `#B8F0D4` | Light green accents |

### Neutral Grays

| Name | Hex | Usage |
|------|-----|-------|
| **Gray 900** | `#1A1A1A` | Primary text |
| **Gray 700** | `#4A4A4A` | Secondary text |
| **Gray 500** | `#8C8C8C` | Muted text, borders |
| **Gray 300** | `#D4D4D4` | Dividers, light borders |
| **Gray 100** | `#F5F5F5` | Light backgrounds |

## Typography

### Font Family
**Avenir Next (for Intuit)** - Custom version with enhanced readability

When Avenir Next is unavailable, use fallbacks:
1. `Avenir Next` (system)
2. `Avenir` 
3. `Nunito Sans` (Google Font alternative)
4. `system-ui, sans-serif`

### Font Weights

| Weight | Name | Usage |
|--------|------|-------|
| 400 | Regular | Body text, descriptions |
| 600 | Demi | Subheadings, emphasis |
| 700 | Bold | Headlines, titles |

### Type Scale for Presentations

| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Title Slide | 54pt | Bold | Super Blue or White |
| Section Header | 44pt | Bold | Midnight or Super Blue |
| Slide Title | 36pt | Demi | Midnight |
| Subtitle | 24pt | Regular | Gray 700 |
| Body Text | 18pt | Regular | Gray 900 |
| Caption | 14pt | Regular | Gray 500 |

## Slide Templates

### 1. Title Slide
- **Background:** Super Blue (#236CFF) or White
- **Title:** 54pt Bold, centered, White (on blue) or Midnight (on white)
- **Subtitle:** 24pt Regular, Gray 300 (on blue) or Gray 700 (on white)
- **Intuit logo:** Bottom right corner, appropriate color version

### 2. Section Divider
- **Background:** Midnight (#0D2644)
- **Section title:** 44pt Bold, White, left-aligned
- **Accent bar:** Super Blue, left edge (I-beam element)

### 3. Content Slide
- **Background:** White
- **Title:** 36pt Demi, Midnight, top left
- **Body:** 18pt Regular, Gray 900
- **Accent elements:** Super Blue for highlights

### 4. Two Column
- **Background:** White or Gray 100
- **Split:** 50/50 or 60/40
- **Divider:** 2px Super Blue line or no divider

### 5. Quote/Highlight
- **Background:** Pale Blue (#E8F1FF)
- **Quote:** 28pt Demi, Midnight
- **Attribution:** 16pt Regular, Gray 700
- **Accent:** Large Super Blue quotation mark

### 6. Data/Metrics
- **Background:** White
- **Numbers:** 72pt Bold, Super Blue
- **Labels:** 18pt Regular, Gray 700
- **Charts:** Use brand colors in order of priority

## Slide Layout Zones

### Standard 16:9 Layout (10" × 5.625")

**CRITICAL:** Always use separate text blocks for title and content areas.

```
┌──────────────────────────────────────────────────────┐
│ ↑ 0.5" top margin                                    │
│ ┌──────────────────────────────────────────────────┐ │
│ │ TITLE ZONE                                       │ │
│ │ x: 0.5"  y: 0.5"  w: 9"  h: 0.7"                │ │
│ └──────────────────────────────────────────────────┘ │
│ ↕ 0.2" gap                                           │
│ ┌──────────────────────────────────────────────────┐ │
│ │                                                  │ │
│ │ CONTENT ZONE                                     │ │
│ │ x: 0.5"  y: 1.4"  w: 9"  h: 3.7"                │ │
│ │                                                  │ │
│ └──────────────────────────────────────────────────┘ │
│ ↓ 0.5" bottom margin                                 │
└──────────────────────────────────────────────────────┘
```

### Layout Constants (in inches)

| Zone | X | Y | Width | Height |
|------|---|---|-------|--------|
| **Title** | 0.5 | 0.5 | 9.0 | 0.7 |
| **Subtitle** | 0.5 | 1.0 | 9.0 | 0.3 |
| **Content** | 0.5 | 1.4 | 9.0 | 3.7 |
| **Footer** | 0.5 | 5.1 | 9.0 | 0.4 |

### With I-Beam Accent (left bar)

When using the I-beam accent bar on the left edge:
- I-beam width: **0.15"** (prominent) or **0.1"** (subtle)
- Adjust content X to **0.5"** (bar is separate, doesn't push content)
- Title and content remain in standard zones

```javascript
// Layout constants for pptxgenjs
const layout = {
  // Margins
  margin: 0.5,
  
  // Title zone
  title: { x: 0.5, y: 0.5, w: 9.0, h: 0.7 },
  
  // Content zone (starts after title + gap)
  content: { x: 0.5, y: 1.4, w: 9.0, h: 3.7 },
  
  // I-beam accent bar
  iBeam: { x: 0, y: 0, w: 0.15, h: '100%' },
  
  // For centered title slides
  centerTitle: { x: 0.5, y: 2.0, w: 9.0, h: 1.2 },
  centerSubtitle: { x: 0.5, y: 3.3, w: 9.0, h: 0.6 }
};
```

## Design Elements

### The I-Beam
The "I" from Intuit serves as a modular design element:
- Use for subtle compositions and framing
- Width: **0.15"** for prominent, **0.1"** for subtle
- Can be used as accent bars or borders
- Fill with Super Blue or gradient

### Spacing
- **Top margin:** 0.5" minimum (never place title closer to top)
- **Side margins:** 0.5" from edges
- **Title-to-content gap:** 0.2" minimum
- **Between content items:** 0.3-0.5"
- **Line height:** 1.4 for body text

### Charts & Graphs
Color application order:
1. Super Blue (#236CFF) - primary data
2. Navy (#1A3D5C) - secondary data
3. Coral (#FF6B6B) - highlight/alert
4. Forest Green (#0A5C36) - positive
5. Amber (#F5A623) - warning
6. Gray 500 (#8C8C8C) - neutral/baseline

## Code Examples

### JavaScript (pptxgenjs)

```javascript
const pptxgen = require('pptxgenjs');

// Intuit Brand Colors
const intuit = {
  superBlue: '236CFF',
  midnight: '0D2644',
  navy: '1A3D5C',
  black: '000000',
  white: 'FFFFFF',
  skyBlue: '5A94FF',
  lightBlue: '8FB8FF',
  iceBlue: 'C4DBFF',
  paleBlue: 'E8F1FF',
  coral: 'FF6B6B',
  forestGreen: '0A5C36',
  amber: 'F5A623',
  gray900: '1A1A1A',
  gray700: '4A4A4A',
  gray500: '8C8C8C',
  gray100: 'F5F5F5'
};

// Create presentation
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
pptx.author = 'Intuit';
pptx.title = 'Presentation Title';

// Title Slide
let slide = pptx.addSlide();
slide.background = { color: intuit.superBlue };
slide.addText('Presentation Title', {
  x: 0.5, y: 2.5, w: '90%',
  fontSize: 54, fontFace: 'Avenir Next', bold: true,
  color: intuit.white, align: 'center'
});
slide.addText('Subtitle goes here', {
  x: 0.5, y: 3.8, w: '90%',
  fontSize: 24, fontFace: 'Avenir Next',
  color: intuit.lightBlue, align: 'center'
});

// Content Slide - with proper layout zones
slide = pptx.addSlide();
slide.background = { color: intuit.white };

// I-beam accent bar (left edge)
slide.addShape('rect', {
  x: 0, y: 0, w: 0.15, h: '100%',
  fill: { color: intuit.superBlue }
});

// TITLE ZONE - separate text block
slide.addText('Slide Title', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,  // Title zone
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight, valign: 'top'
});

// CONTENT ZONE - separate text block
slide.addText('Body content goes here...', {
  x: 0.5, y: 1.4, w: 9.0, h: 3.7,  // Content zone
  fontSize: 18, fontFace: 'Avenir Next',
  color: intuit.gray700, valign: 'top'
});

// Section Divider
slide = pptx.addSlide();
slide.background = { color: intuit.midnight };
slide.addShape('rect', {
  x: 0, y: 0, w: 0.15, h: '100%',
  fill: { color: intuit.superBlue }
});
slide.addText('Section Title', {
  x: 0.5, y: 2.3, w: '80%',
  fontSize: 44, fontFace: 'Avenir Next', bold: true,
  color: intuit.white
});

pptx.writeFile({ fileName: 'intuit-presentation.pptx' });
```

### Color Utility Functions

```javascript
// Convert hex to PowerPoint format (no #)
const toColor = (hex) => hex.replace('#', '');

// Get complementary color pair
const getColorPair = (type) => {
  const pairs = {
    primary: { bg: intuit.superBlue, text: intuit.white },
    dark: { bg: intuit.midnight, text: intuit.white },
    light: { bg: intuit.white, text: intuit.midnight },
    subtle: { bg: intuit.paleBlue, text: intuit.midnight },
    alert: { bg: intuit.coral, text: intuit.white },
    success: { bg: intuit.forestGreen, text: intuit.white }
  };
  return pairs[type] || pairs.light;
};
```

## Best Practices

### Do
- ✅ Use Super Blue as the dominant accent color
- ✅ Maintain generous white space
- ✅ Use bold typography for headlines
- ✅ Keep slide content focused (one idea per slide)
- ✅ Use the I-beam element for subtle branding
- ✅ Ensure high contrast for accessibility

### Don't
- ❌ Use colors outside the brand palette
- ❌ Crowd slides with too much text
- ❌ Use decorative fonts
- ❌ Place text over busy backgrounds without overlay
- ❌ Use gradients except where specifically approved
- ❌ Stretch or distort the Intuit logo

## Accessibility

- Minimum contrast ratio: 4.5:1 for body text
- Use Super Blue on white (contrast 4.67:1) ✓
- Use Midnight on white (contrast 15.2:1) ✓
- Avoid red/green combinations alone
- Include alt text for all images

## References

- [Intuit Visual Identity](https://visual.intuit.com)
- [Intuit Design Hub](https://design.intuit.com)
- [QuickBooks Brand Guidelines](https://design.intuit.com/quickbooks/brand/)

---

*This skill was created based on publicly available brand guidelines from visual.intuit.com (2023 visual identity) and design.intuit.com.*

