/**
 * Micron Technology Investment POV - PowerPoint Presentation
 * Created using Intuit brand guidelines from visual.intuit.com
 * 
 * Colors: Super Blue (#236CFF), Midnight (#0D2644), etc.
 * Typography: Avenir Next
 */

const pptxgen = require('pptxgenjs');

// ============================================================================
// INTUIT BRAND COLORS (from visual.intuit.com)
// ============================================================================
const intuit = {
  // Primary Colors
  superBlue: '236CFF',
  midnight: '0D2644',
  navy: '1A3D5C',
  black: '000000',
  white: 'FFFFFF',
  
  // Light Blues
  skyBlue: '5A94FF',
  lightBlue: '8FB8FF',
  iceBlue: 'C4DBFF',
  paleBlue: 'E8F1FF',
  
  // Secondary Colors
  burgundy: '5C1F35',
  coral: 'FF6B6B',
  pink: 'FFB4C4',
  amber: 'F5A623',
  gold: 'FFCC4D',
  cream: 'FFF4D9',
  forestGreen: '0A5C36',
  green: '2ECC71',
  mint: 'B8F0D4',
  
  // Neutral Grays
  gray900: '1A1A1A',
  gray700: '4A4A4A',
  gray500: '8C8C8C',
  gray300: 'D4D4D4',
  gray100: 'F5F5F5'
};

// ============================================================================
// CREATE PRESENTATION
// ============================================================================
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
pptx.author = 'Investment Research';
pptx.title = 'Micron Technology Investment POV';
pptx.subject = 'MU Stock Analysis - January 2026';
pptx.company = 'Research';

// ============================================================================
// SLIDE 1: TITLE SLIDE
// ============================================================================
let slide = pptx.addSlide();
slide.background = { color: intuit.midnight };

// Accent bar
slide.addShape('rect', {
  x: 0, y: 0, w: 0.15, h: '100%',
  fill: { color: intuit.superBlue }
});

slide.addText('Micron Technology', {
  x: 0.5, y: 1.8, w: 9.0, h: 0.9,
  fontSize: 54, fontFace: 'Avenir Next', bold: true,
  color: intuit.white, align: 'center'
});

slide.addText('The AI Memory Powerhouse', {
  x: 0.5, y: 2.7, w: 9.0, h: 0.6,
  fontSize: 28, fontFace: 'Avenir Next',
  color: intuit.skyBlue, align: 'center'
});

slide.addText('Investment Point of View | NASDAQ: MU', {
  x: 0.5, y: 3.5, w: 9.0, h: 0.5,
  fontSize: 20, fontFace: 'Avenir Next',
  color: intuit.lightBlue, align: 'center'
});

slide.addText('January 2026', {
  x: 0.5, y: 4.2, w: 9.0, h: 0.4,
  fontSize: 16, fontFace: 'Avenir Next',
  color: intuit.iceBlue, align: 'center'
});

// Stock price highlight
slide.addShape('rect', {
  x: 3.5, y: 4.8, w: 3.0, h: 0.6,
  fill: { color: intuit.superBlue }
});

slide.addText('$315.42  |  +173% YTD', {
  x: 3.5, y: 4.85, w: 3.0, h: 0.5,
  fontSize: 14, fontFace: 'Avenir Next', bold: true,
  color: intuit.white, align: 'center', valign: 'middle'
});

// ============================================================================
// SLIDE 2: EXECUTIVE SUMMARY
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };

slide.addShape('rect', {
  x: 0, y: 0, w: 0.15, h: '100%',
  fill: { color: intuit.superBlue }
});

slide.addText('Executive Summary', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

const execSummary = [
  { text: 'Micron is at the center of the AI infrastructure revolution. ', options: { bold: true, color: intuit.gray900 } },
  { text: 'As one of only three major memory manufacturers globally, Micron has emerged as a critical enabler of AI compute.\n\n', options: { color: intuit.gray700 } },
  { text: 'FY2025 Performance: ', options: { bold: true, color: intuit.superBlue } },
  { text: '$37.38B revenue (+48.9% YoY), $8.54B profit (vs $5.83B loss prior year)\n\n', options: { color: intuit.gray700 } },
  { text: 'Key Catalyst: ', options: { bold: true, color: intuit.superBlue } },
  { text: 'HBM4 technology leadership with 2.8TB/s bandwidth, ahead of Samsung and SK Hynix\n\n', options: { color: intuit.gray700 } },
  { text: 'Technical Position: ', options: { bold: true, color: intuit.superBlue } },
  { text: 'Stock up 173% YTD, RSI 69.62 approaching overbought. Consider entry on pullback.', options: { color: intuit.gray700 } }
];

slide.addText(execSummary, {
  x: 0.5, y: 1.4, w: 9.0, h: 3.5,
  fontSize: 16, fontFace: 'Avenir Next',
  valign: 'top'
});

// ============================================================================
// SLIDE 3: WHY MICRON MATTERS
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: intuit.superBlue };

slide.addText('Why Micron Matters', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.white
});

slide.addText('The AI Memory Equation', {
  x: 0.5, y: 1.2, w: 9.0, h: 0.4,
  fontSize: 20, fontFace: 'Avenir Next',
  color: intuit.iceBlue
});

const whyMatters = [
  { icon: '⚡', text: 'Every AI training run requires massive high-speed memory' },
  { icon: '🧠', text: 'Every LLM inference needs HBM for bandwidth-intensive operations' },
  { icon: '📈', text: 'Data center DRAM demand growing 20%+ annually through 2028' },
  { icon: '🚀', text: 'HBM demand expected to grow 5x by 2028' }
];

whyMatters.forEach((item, i) => {
  slide.addText([
    { text: item.icon + '  ', options: { fontSize: 22 } },
    { text: item.text, options: { fontSize: 18 } }
  ], {
    x: 0.5, y: 1.8 + (i * 0.7), w: 9.0, h: 0.6,
    fontFace: 'Avenir Next', color: intuit.white, valign: 'middle'
  });
});

// Bottom highlight box
slide.addShape('rect', {
  x: 0.5, y: 4.5, w: 9.0, h: 0.8,
  fill: { color: intuit.midnight }
});

slide.addText('Only 3 companies make HBM: Samsung, SK Hynix, and Micron', {
  x: 0.7, y: 4.6, w: 8.6, h: 0.6,
  fontSize: 16, fontFace: 'Avenir Next', bold: true,
  color: intuit.white, align: 'center', valign: 'middle'
});

// ============================================================================
// SLIDE 4: COMPANY OVERVIEW
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };

slide.addShape('rect', {
  x: 0, y: 0, w: 0.15, h: '100%',
  fill: { color: intuit.superBlue }
});

slide.addText('Company Overview', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

// Key Stats Table
const statsRows = [
  [
    { text: 'Founded', options: { bold: true, color: intuit.superBlue } },
    { text: '1978 (47 years)', options: { color: intuit.gray700 } },
    { text: 'Revenue (FY25)', options: { bold: true, color: intuit.superBlue } },
    { text: '$37.38B', options: { color: intuit.gray700 } }
  ],
  [
    { text: 'Headquarters', options: { bold: true, color: intuit.superBlue } },
    { text: 'Boise, Idaho', options: { color: intuit.gray700 } },
    { text: 'Net Income', options: { bold: true, color: intuit.superBlue } },
    { text: '$8.54B', options: { color: intuit.gray700 } }
  ],
  [
    { text: 'CEO', options: { bold: true, color: intuit.superBlue } },
    { text: 'Sanjay Mehrotra', options: { color: intuit.gray700 } },
    { text: 'Market Cap', options: { bold: true, color: intuit.superBlue } },
    { text: '$353B', options: { color: intuit.gray700 } }
  ],
  [
    { text: 'Employees', options: { bold: true, color: intuit.superBlue } },
    { text: '~48,000', options: { color: intuit.gray700 } },
    { text: 'Stock Price', options: { bold: true, color: intuit.superBlue } },
    { text: '$315.42', options: { color: intuit.gray700 } }
  ]
];

slide.addTable(statsRows, {
  x: 0.5, y: 1.3, w: 9.0, h: 1.8,
  fontSize: 14, fontFace: 'Avenir Next',
  border: { type: 'solid', pt: 0.5, color: intuit.gray300 },
  fill: { color: intuit.paleBlue },
  align: 'left',
  valign: 'middle',
  colW: [1.8, 2.7, 1.8, 2.7]
});

// Memory Technologies
slide.addText('Memory Technology Portfolio', {
  x: 0.5, y: 3.3, w: 9.0, h: 0.4,
  fontSize: 18, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

const techRows = [
  [
    { text: 'Technology', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } },
    { text: 'Description', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } },
    { text: 'Application', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } }
  ],
  ['HBM (High Bandwidth Memory)', 'Stacked memory for AI accelerators', 'NVIDIA GPUs, AI Training'],
  ['DDR5 DRAM', 'Latest gen server memory', 'Data Centers, Cloud'],
  ['LPDDR5X', 'Low-power mobile memory', 'Smartphones, Edge AI'],
  ['NAND Flash', 'Storage memory', 'Enterprise SSDs']
];

slide.addTable(techRows, {
  x: 0.5, y: 3.7, w: 9.0, h: 1.5,
  fontSize: 12, fontFace: 'Avenir Next',
  color: intuit.gray700,
  border: { type: 'solid', pt: 0.5, color: intuit.gray300 },
  align: 'center',
  valign: 'middle',
  colW: [3.0, 3.5, 2.5]
});

// ============================================================================
// SLIDE 5: HBM TECHNOLOGY LEADERSHIP
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: intuit.midnight };

slide.addShape('rect', {
  x: 0, y: 0, w: 0.15, h: '100%',
  fill: { color: intuit.superBlue }
});

slide.addText('HBM Technology Leadership', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.white
});

slide.addText('Micron shipped HBM4 samples with 2.8TB/s bandwidth — the fastest HBM ever made', {
  x: 0.5, y: 1.2, w: 9.0, h: 0.5,
  fontSize: 16, fontFace: 'Avenir Next', italic: true,
  color: intuit.skyBlue
});

// Comparison Table
const hbmComparison = [
  [
    { text: 'Company', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } },
    { text: 'HBM Gen', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } },
    { text: 'Bandwidth', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } },
    { text: 'Status', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } }
  ],
  [
    { text: '🏆 MICRON', options: { bold: true, fill: { color: intuit.forestGreen }, color: intuit.white } },
    { text: 'HBM4', options: { bold: true, fill: { color: intuit.forestGreen }, color: intuit.white } },
    { text: '2.8TB/s', options: { bold: true, fill: { color: intuit.forestGreen }, color: intuit.white } },
    { text: 'SAMPLING', options: { bold: true, fill: { color: intuit.forestGreen }, color: intuit.white } }
  ],
  [
    { text: 'Samsung', options: { fill: { color: intuit.gray100 } } },
    { text: 'HBM3E', options: { fill: { color: intuit.gray100 } } },
    { text: '1.2TB/s', options: { fill: { color: intuit.gray100 } } },
    { text: 'Production', options: { fill: { color: intuit.gray100 } } }
  ],
  [
    { text: 'SK Hynix', options: { fill: { color: intuit.white } } },
    { text: 'HBM3E', options: { fill: { color: intuit.white } } },
    { text: '1.2TB/s', options: { fill: { color: intuit.white } } },
    { text: 'Production', options: { fill: { color: intuit.white } } }
  ]
];

slide.addTable(hbmComparison, {
  x: 0.5, y: 1.9, w: 9.0, h: 1.8,
  fontSize: 14, fontFace: 'Avenir Next',
  color: intuit.gray700,
  border: { type: 'solid', pt: 1, color: intuit.gray500 },
  align: 'center',
  valign: 'middle',
  colW: [2.5, 2.0, 2.25, 2.25]
});

// Why it matters
slide.addText('Why This Matters', {
  x: 0.5, y: 4.0, w: 9.0, h: 0.4,
  fontSize: 18, fontFace: 'Avenir Next', bold: true,
  color: intuit.white
});

slide.addText([
  { text: '• NVIDIA\'s Blackwell GPUs will use HBM3E/HBM4\n', options: { color: intuit.lightBlue } },
  { text: '• Being first to market positions Micron as strategic supplier\n', options: { color: intuit.lightBlue } },
  { text: '• 2.3x faster than competing HBM3E solutions', options: { color: intuit.lightBlue } }
], {
  x: 0.5, y: 4.4, w: 9.0, h: 1.0,
  fontSize: 14, fontFace: 'Avenir Next'
});

// ============================================================================
// SLIDE 6: FINANCIAL TURNAROUND
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };

slide.addShape('rect', {
  x: 0, y: 0, w: 0.15, h: '100%',
  fill: { color: intuit.superBlue }
});

slide.addText('The Financial Turnaround', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

// Big numbers showing turnaround
slide.addText('FY2024', {
  x: 0.5, y: 1.4, w: 4.2, h: 0.3,
  fontSize: 14, fontFace: 'Avenir Next',
  color: intuit.gray500, align: 'center'
});

slide.addText('-$5.83B', {
  x: 0.5, y: 1.7, w: 4.2, h: 0.8,
  fontSize: 48, fontFace: 'Avenir Next', bold: true,
  color: intuit.coral, align: 'center'
});

slide.addText('Net Loss', {
  x: 0.5, y: 2.5, w: 4.2, h: 0.3,
  fontSize: 14, fontFace: 'Avenir Next',
  color: intuit.gray500, align: 'center'
});

// Arrow
slide.addText('→', {
  x: 4.2, y: 1.8, w: 1.0, h: 0.6,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.superBlue, align: 'center'
});

slide.addText('FY2025', {
  x: 5.3, y: 1.4, w: 4.2, h: 0.3,
  fontSize: 14, fontFace: 'Avenir Next',
  color: intuit.gray500, align: 'center'
});

slide.addText('+$8.54B', {
  x: 5.3, y: 1.7, w: 4.2, h: 0.8,
  fontSize: 48, fontFace: 'Avenir Next', bold: true,
  color: intuit.forestGreen, align: 'center'
});

slide.addText('Net Income', {
  x: 5.3, y: 2.5, w: 4.2, h: 0.3,
  fontSize: 14, fontFace: 'Avenir Next',
  color: intuit.gray500, align: 'center'
});

// Swing highlight
slide.addShape('rect', {
  x: 2.5, y: 3.0, w: 5.0, h: 0.5,
  fill: { color: intuit.paleBlue },
  line: { color: intuit.superBlue, pt: 2 }
});

slide.addText('$14.4B EARNINGS SWING', {
  x: 2.5, y: 3.05, w: 5.0, h: 0.4,
  fontSize: 18, fontFace: 'Avenir Next', bold: true,
  color: intuit.superBlue, align: 'center', valign: 'middle'
});

// Key metrics
const finMetrics = [
  { label: 'Revenue', value: '$37.38B', growth: '+48.9%' },
  { label: 'Gross Profit', value: '$14.87B', growth: 'Recovery' },
  { label: 'Op Cash Flow', value: '$17.5B', growth: '+106%' }
];

finMetrics.forEach((m, i) => {
  const x = 0.5 + (i * 3.0);
  
  slide.addText(m.value, {
    x: x, y: 3.8, w: 2.8, h: 0.5,
    fontSize: 28, fontFace: 'Avenir Next', bold: true,
    color: intuit.superBlue, align: 'center'
  });
  
  slide.addText(m.label, {
    x: x, y: 4.3, w: 2.8, h: 0.3,
    fontSize: 14, fontFace: 'Avenir Next',
    color: intuit.gray700, align: 'center'
  });
  
  slide.addText(m.growth + ' YoY', {
    x: x, y: 4.6, w: 2.8, h: 0.3,
    fontSize: 12, fontFace: 'Avenir Next', bold: true,
    color: intuit.forestGreen, align: 'center'
  });
});

// ============================================================================
// SLIDE 7: FINANCIAL RATIOS
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };

slide.addShape('rect', {
  x: 0, y: 0, w: 0.15, h: '100%',
  fill: { color: intuit.superBlue }
});

slide.addText('Financial Health Check', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

// Valuation ratios
slide.addText('Valuation', {
  x: 0.5, y: 1.3, w: 4.2, h: 0.4,
  fontSize: 18, fontFace: 'Avenir Next', bold: true,
  color: intuit.superBlue
});

const valRows = [
  ['P/E Ratio', '29.93x', '✓ Fair'],
  ['Price/Sales', '3.64x', '✓ Moderate'],
  ['Price/Book', '2.51x', '✓ Reasonable'],
  ['EV/EBITDA', '7.67x', '✓ Cheap']
];

slide.addTable(valRows, {
  x: 0.5, y: 1.7, w: 4.2, h: 1.6,
  fontSize: 13, fontFace: 'Avenir Next',
  color: intuit.gray700,
  border: { type: 'solid', pt: 0.5, color: intuit.gray300 },
  fill: { color: intuit.paleBlue },
  align: 'center',
  valign: 'middle',
  colW: [1.6, 1.3, 1.3]
});

// Quality ratios
slide.addText('Quality & Strength', {
  x: 5.3, y: 1.3, w: 4.2, h: 0.4,
  fontSize: 18, fontFace: 'Avenir Next', bold: true,
  color: intuit.superBlue
});

const qualRows = [
  ['ROE', '15.8%', '✓ Strong'],
  ['ROA', '10.3%', '✓ Efficient'],
  ['Current Ratio', '2.52', '✓ Liquid'],
  ['Debt/Equity', '0.28', '✓ Low']
];

slide.addTable(qualRows, {
  x: 5.3, y: 1.7, w: 4.2, h: 1.6,
  fontSize: 13, fontFace: 'Avenir Next',
  color: intuit.gray700,
  border: { type: 'solid', pt: 0.5, color: intuit.gray300 },
  fill: { color: intuit.paleBlue },
  align: 'center',
  valign: 'middle',
  colW: [1.6, 1.3, 1.3]
});

// Assessment
slide.addShape('rect', {
  x: 0.5, y: 3.6, w: 9.0, h: 1.5,
  fill: { color: intuit.midnight }
});

slide.addText('Valuation Assessment', {
  x: 0.7, y: 3.7, w: 8.6, h: 0.4,
  fontSize: 16, fontFace: 'Avenir Next', bold: true,
  color: intuit.white
});

slide.addText('Micron trades at a discount to semiconductor peers (25-35x P/E avg) despite technology leadership and structural AI tailwinds. The discount reflects memory\'s historical cyclicality. If AI memory demand proves more durable, multiple expansion is likely.', {
  x: 0.7, y: 4.1, w: 8.6, h: 0.9,
  fontSize: 13, fontFace: 'Avenir Next',
  color: intuit.lightBlue
});

// ============================================================================
// SLIDE 8: TECHNICAL ANALYSIS
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };

slide.addShape('rect', {
  x: 0, y: 0, w: 0.15, h: '100%',
  fill: { color: intuit.superBlue }
});

slide.addText('Technical Analysis', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

// Performance boxes
const perfData = [
  { period: '1 Day', perf: '+10.51%', color: intuit.forestGreen },
  { period: '1 Month', perf: '+39.17%', color: intuit.forestGreen },
  { period: '1 Year', perf: '+173.61%', color: intuit.forestGreen }
];

perfData.forEach((p, i) => {
  const x = 0.5 + (i * 3.0);
  
  slide.addShape('rect', {
    x: x, y: 1.3, w: 2.8, h: 0.9,
    fill: { color: intuit.paleBlue },
    line: { color: p.color, pt: 2 }
  });
  
  slide.addText(p.perf, {
    x: x, y: 1.35, w: 2.8, h: 0.5,
    fontSize: 24, fontFace: 'Avenir Next', bold: true,
    color: p.color, align: 'center'
  });
  
  slide.addText(p.period, {
    x: x, y: 1.85, w: 2.8, h: 0.3,
    fontSize: 12, fontFace: 'Avenir Next',
    color: intuit.gray700, align: 'center'
  });
});

// Technical indicators table
const techIndicators = [
  ['Indicator', 'Value', 'Signal'],
  ['SMA 20', '$262.43', 'Price Above ✓'],
  ['SMA 50', '$242.27', 'Price Above ✓'],
  ['SMA 200', '$149.15', 'Price Above ✓'],
  ['RSI (14)', '69.62', '⚠️ Near Overbought'],
  ['MACD', '+4.44', 'Bullish ✓']
];

slide.addTable(techIndicators, {
  x: 0.5, y: 2.4, w: 5.5, h: 2.0,
  fontSize: 13, fontFace: 'Avenir Next',
  color: intuit.gray700,
  border: { type: 'solid', pt: 0.5, color: intuit.gray300 },
  align: 'center',
  valign: 'middle',
  colW: [1.8, 1.8, 1.9]
});

// Support/Resistance
slide.addText('Key Levels', {
  x: 6.2, y: 2.4, w: 3.3, h: 0.4,
  fontSize: 16, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

slide.addText([
  { text: 'RESISTANCE\n', options: { bold: true, color: intuit.coral, fontSize: 12 } },
  { text: '$329 (R2)\n$322 (R1)\n$316 (52W High)\n\n', options: { color: intuit.gray700, fontSize: 11 } },
  { text: 'SUPPORT\n', options: { bold: true, color: intuit.forestGreen, fontSize: 12 } },
  { text: '$308 (Pivot)\n$262 (SMA 20)\n$242 (SMA 50)', options: { color: intuit.gray700, fontSize: 11 } }
], {
  x: 6.2, y: 2.8, w: 3.3, h: 2.0,
  fontFace: 'Avenir Next', valign: 'top'
});

// Trend assessment
slide.addText([
  { text: 'TREND: ', options: { bold: true, color: intuit.superBlue } },
  { text: 'Strong Uptrend  |  ', options: { color: intuit.gray700 } },
  { text: 'MOMENTUM: ', options: { bold: true, color: intuit.superBlue } },
  { text: 'Bullish but Extended  |  ', options: { color: intuit.gray700 } },
  { text: 'VOLUME: ', options: { bold: true, color: intuit.superBlue } },
  { text: '1.5x Above Average', options: { color: intuit.gray700 } }
], {
  x: 0.5, y: 4.7, w: 9.0, h: 0.4,
  fontSize: 12, fontFace: 'Avenir Next'
});

// ============================================================================
// SLIDE 9: STRATEGIC INITIATIVES
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };

slide.addShape('rect', {
  x: 0, y: 0, w: 0.15, h: '100%',
  fill: { color: intuit.superBlue }
});

slide.addText('Strategic Initiatives', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

// Initiative 1: HBM
slide.addShape('rect', {
  x: 0.5, y: 1.3, w: 4.2, h: 1.8,
  fill: { color: intuit.paleBlue },
  line: { color: intuit.superBlue, pt: 1 }
});

slide.addText('🎯 HBM Leadership', {
  x: 0.6, y: 1.4, w: 4.0, h: 0.4,
  fontSize: 16, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

slide.addText('• HBM3E in production now\n• HBM4 sampling (2.8TB/s)\n• HBM4E in development\n• Goal: 25%+ market share by 2027', {
  x: 0.6, y: 1.8, w: 4.0, h: 1.2,
  fontSize: 12, fontFace: 'Avenir Next',
  color: intuit.gray700
});

// Initiative 2: Capacity
slide.addShape('rect', {
  x: 5.3, y: 1.3, w: 4.2, h: 1.8,
  fill: { color: intuit.paleBlue },
  line: { color: intuit.superBlue, pt: 1 }
});

slide.addText('🏭 Manufacturing Expansion', {
  x: 5.4, y: 1.4, w: 4.0, h: 0.4,
  fontSize: 16, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

slide.addText('• Japan HBM Fab: $9.6B (2028)\n• Idaho Fab: $15B+ (US hub)\n• Singapore: $5B+ expansion\n• CHIPS Act support', {
  x: 5.4, y: 1.8, w: 4.0, h: 1.2,
  fontSize: 12, fontFace: 'Avenir Next',
  color: intuit.gray700
});

// Initiative 3: Consumer Exit
slide.addShape('rect', {
  x: 0.5, y: 3.3, w: 4.2, h: 1.5,
  fill: { color: intuit.paleBlue },
  line: { color: intuit.superBlue, pt: 1 }
});

slide.addText('🔄 Enterprise Focus', {
  x: 0.6, y: 3.4, w: 4.0, h: 0.4,
  fontSize: 16, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

slide.addText('• Exiting Crucial brand (Feb 2026)\n• Focus on high-margin enterprise\n• Capital allocation to AI/HBM\n• Positive margin mix shift', {
  x: 0.6, y: 3.8, w: 4.0, h: 1.0,
  fontSize: 12, fontFace: 'Avenir Next',
  color: intuit.gray700
});

// Initiative 4: Data Center
slide.addShape('rect', {
  x: 5.3, y: 3.3, w: 4.2, h: 1.5,
  fill: { color: intuit.paleBlue },
  line: { color: intuit.superBlue, pt: 1 }
});

slide.addText('💾 Data Center Leadership', {
  x: 5.4, y: 3.4, w: 4.0, h: 0.4,
  fontSize: 16, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

slide.addText('• DDR5 adoption accelerating\n• CXL memory expansion\n• Compute Express Link\n• Memory pooling technology', {
  x: 5.4, y: 3.8, w: 4.0, h: 1.0,
  fontSize: 12, fontFace: 'Avenir Next',
  color: intuit.gray700
});

// ============================================================================
// SLIDE 10: COMPETITIVE LANDSCAPE
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };

slide.addShape('rect', {
  x: 0, y: 0, w: 0.15, h: '100%',
  fill: { color: intuit.superBlue }
});

slide.addText('Competitive Landscape', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

slide.addText('The Memory Triopoly', {
  x: 0.5, y: 1.1, w: 9.0, h: 0.4,
  fontSize: 18, fontFace: 'Avenir Next',
  color: intuit.gray700
});

// Market share table
const marketShare = [
  [
    { text: 'Company', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } },
    { text: 'DRAM Share', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } },
    { text: 'HBM Position', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } },
    { text: 'Key Strength', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } }
  ],
  ['Samsung', '~42%', 'Strong (HBM3E)', 'Scale & Resources'],
  ['SK Hynix', '~29%', 'NVIDIA Primary', 'Customer Lock-in'],
  [
    { text: 'Micron', options: { bold: true } },
    { text: '~25%', options: { bold: true } },
    { text: 'HBM4 Leader', options: { bold: true, color: intuit.forestGreen } },
    { text: 'Technology Edge', options: { bold: true } }
  ]
];

slide.addTable(marketShare, {
  x: 0.5, y: 1.5, w: 9.0, h: 1.4,
  fontSize: 13, fontFace: 'Avenir Next',
  color: intuit.gray700,
  border: { type: 'solid', pt: 0.5, color: intuit.gray300 },
  align: 'center',
  valign: 'middle',
  colW: [2.0, 2.0, 2.5, 2.5]
});

// Advantages vs Risks
slide.addText('Competitive Advantages', {
  x: 0.5, y: 3.1, w: 4.2, h: 0.4,
  fontSize: 16, fontFace: 'Avenir Next', bold: true,
  color: intuit.forestGreen
});

slide.addText('✓ First to market with HBM4\n✓ US manufacturing (CHIPS Act)\n✓ Vertical integration\n✓ $3B+ annual R&D investment', {
  x: 0.5, y: 3.5, w: 4.2, h: 1.4,
  fontSize: 12, fontFace: 'Avenir Next',
  color: intuit.gray700
});

slide.addText('Key Risks to Monitor', {
  x: 5.3, y: 3.1, w: 4.2, h: 0.4,
  fontSize: 16, fontFace: 'Avenir Next', bold: true,
  color: intuit.coral
});

slide.addText('⚠ Samsung scale advantage\n⚠ SK Hynix NVIDIA relationship\n⚠ China geopolitical exposure\n⚠ Memory cycle volatility', {
  x: 5.3, y: 3.5, w: 4.2, h: 1.4,
  fontSize: 12, fontFace: 'Avenir Next',
  color: intuit.gray700
});

// ============================================================================
// SLIDE 11: INVESTMENT RECOMMENDATION
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: intuit.superBlue };

slide.addText('Investment Recommendation', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.white
});

// Recommendation box
slide.addShape('rect', {
  x: 0.5, y: 1.3, w: 9.0, h: 1.0,
  fill: { color: intuit.white },
  shadow: { type: 'outer', blur: 8, offset: 4, angle: 45, opacity: 0.2 }
});

slide.addText('BUY ON PULLBACK', {
  x: 0.5, y: 1.4, w: 9.0, h: 0.6,
  fontSize: 40, fontFace: 'Avenir Next', bold: true,
  color: intuit.forestGreen, align: 'center', valign: 'middle'
});

slide.addText('Wait for RSI to cool / Target entry: $260-280 range', {
  x: 0.5, y: 2.0, w: 9.0, h: 0.3,
  fontSize: 14, fontFace: 'Avenir Next',
  color: intuit.gray700, align: 'center'
});

// Rationale
const rationale = [
  { label: 'Structural Tailwind', desc: 'AI memory demand is a multi-year growth driver' },
  { label: 'Technology Leadership', desc: 'HBM4 positions Micron ahead of competitors' },
  { label: 'Turnaround Confirmed', desc: '$14.4B earnings swing proves execution' },
  { label: 'Tactical Caution', desc: 'Stock extended (+173%), RSI 69.62 near overbought' }
];

rationale.forEach((r, i) => {
  slide.addText([
    { text: r.label + '\n', options: { bold: true, color: intuit.white, fontSize: 14 } },
    { text: r.desc, options: { color: intuit.lightBlue, fontSize: 12 } }
  ], {
    x: 0.5, y: 2.5 + (i * 0.65), w: 9.0, h: 0.6,
    fontFace: 'Avenir Next', valign: 'top'
  });
});

// ============================================================================
// SLIDE 12: PRICE TARGETS
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };

slide.addShape('rect', {
  x: 0, y: 0, w: 0.15, h: '100%',
  fill: { color: intuit.superBlue }
});

slide.addText('Price Targets & Entry Strategy', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

// Price target boxes
const targets = [
  { scenario: 'Bull Case', price: '$420', change: '+33%', color: intuit.forestGreen },
  { scenario: 'Base Case', price: '$380', change: '+21%', color: intuit.superBlue },
  { scenario: 'Bear Case', price: '$220', change: '-30%', color: intuit.coral }
];

targets.forEach((t, i) => {
  const x = 0.5 + (i * 3.0);
  
  slide.addShape('rect', {
    x: x, y: 1.3, w: 2.8, h: 1.3,
    fill: { color: intuit.paleBlue },
    line: { color: t.color, pt: 3 }
  });
  
  slide.addText(t.scenario, {
    x: x, y: 1.4, w: 2.8, h: 0.3,
    fontSize: 13, fontFace: 'Avenir Next', bold: true,
    color: intuit.gray700, align: 'center'
  });
  
  slide.addText(t.price, {
    x: x, y: 1.7, w: 2.8, h: 0.5,
    fontSize: 32, fontFace: 'Avenir Next', bold: true,
    color: t.color, align: 'center'
  });
  
  slide.addText(t.change, {
    x: x, y: 2.2, w: 2.8, h: 0.3,
    fontSize: 14, fontFace: 'Avenir Next',
    color: intuit.gray700, align: 'center'
  });
});

// Entry strategy
slide.addText('Entry Strategy', {
  x: 0.5, y: 2.9, w: 9.0, h: 0.4,
  fontSize: 18, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

const entryStrategy = [
  { text: 'Aggressive Entry: ', options: { bold: true, color: intuit.superBlue } },
  { text: 'Current levels ($315) for conviction holders\n', options: { color: intuit.gray700 } },
  { text: 'Preferred Entry: ', options: { bold: true, color: intuit.superBlue } },
  { text: 'Pullback to $260-280 range (near SMA 20/50)\n', options: { color: intuit.gray700 } },
  { text: 'Conservative Entry: ', options: { bold: true, color: intuit.superBlue } },
  { text: 'Wait for RSI to cool below 50\n', options: { color: intuit.gray700 } },
  { text: 'Stop Loss: ', options: { bold: true, color: intuit.coral } },
  { text: 'Below $200 (major support break)', options: { color: intuit.gray700 } }
];

slide.addText(entryStrategy, {
  x: 0.5, y: 3.3, w: 9.0, h: 1.4,
  fontSize: 14, fontFace: 'Avenir Next',
  valign: 'top'
});

// Position sizing
slide.addShape('rect', {
  x: 0.5, y: 4.8, w: 9.0, h: 0.5,
  fill: { color: intuit.paleBlue }
});

slide.addText('Position Sizing:  Conservative 2-4%  |  Moderate 4-6%  |  Aggressive 6-8%', {
  x: 0.5, y: 4.85, w: 9.0, h: 0.4,
  fontSize: 13, fontFace: 'Avenir Next',
  color: intuit.gray700, align: 'center', valign: 'middle'
});

// ============================================================================
// SLIDE 13: KEY TAKEAWAYS
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: intuit.midnight };

slide.addShape('rect', {
  x: 0, y: 0, w: 0.15, h: '100%',
  fill: { color: intuit.superBlue }
});

slide.addText('Key Takeaways', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.white
});

const takeaways = [
  { icon: '🏆', text: 'Technology leader in HBM with 2.8TB/s HBM4 bandwidth' },
  { icon: '📈', text: 'Massive turnaround: $5.83B loss → $8.54B profit' },
  { icon: '🚀', text: 'Structural growth from AI memory supercycle' },
  { icon: '🎯', text: 'Strategic pivot to high-margin enterprise products' },
  { icon: '⚠️', text: 'Stock extended (+173% YTD) — wait for pullback' }
];

takeaways.forEach((item, i) => {
  slide.addText([
    { text: item.icon + '  ', options: { fontSize: 20 } },
    { text: item.text, options: { fontSize: 17 } }
  ], {
    x: 0.5, y: 1.4 + (i * 0.7), w: 9.0, h: 0.6,
    fontFace: 'Avenir Next', color: intuit.lightBlue, valign: 'middle'
  });
});

// Bottom line
slide.addShape('rect', {
  x: 0.5, y: 4.3, w: 9.0, h: 1.0,
  fill: { color: intuit.superBlue }
});

slide.addText('Micron is one of the best ways to play AI infrastructure. The stock has moved significantly, but the fundamental story is intact. Patience for a pullback improves risk/reward.', {
  x: 0.7, y: 4.4, w: 8.6, h: 0.8,
  fontSize: 13, fontFace: 'Avenir Next', italic: true,
  color: intuit.white, align: 'center', valign: 'middle'
});

// ============================================================================
// SLIDE 14: CLOSING
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: intuit.superBlue };

slide.addText('Thank You', {
  x: 0.5, y: 2.0, w: 9.0, h: 1.0,
  fontSize: 54, fontFace: 'Avenir Next', bold: true,
  color: intuit.white, align: 'center'
});

slide.addText('Micron Technology Investment POV | January 2026', {
  x: 0.5, y: 3.2, w: 9.0, h: 0.5,
  fontSize: 18, fontFace: 'Avenir Next',
  color: intuit.lightBlue, align: 'center'
});

slide.addText('NASDAQ: MU  |  $315.42  |  +173% YTD', {
  x: 0.5, y: 3.8, w: 9.0, h: 0.4,
  fontSize: 14, fontFace: 'Avenir Next',
  color: intuit.iceBlue, align: 'center'
});

slide.addText('Powering the AI Memory Revolution', {
  x: 0.5, y: 4.8, w: 9.0, h: 0.4,
  fontSize: 14, fontFace: 'Avenir Next', italic: true,
  color: intuit.paleBlue, align: 'center'
});

// ============================================================================
// SAVE PRESENTATION
// ============================================================================
const outputPath = '/Users/snandwani2/personal/research/micron-pov-2026/Micron-Investment-POV-Jan2026.pptx';
pptx.writeFile({ fileName: outputPath })
  .then(() => {
    console.log('✅ Presentation created successfully!');
    console.log(`📁 Output: ${outputPath}`);
    console.log('');
    console.log('Slides created:');
    console.log('  1. Title Slide');
    console.log('  2. Executive Summary');
    console.log('  3. Why Micron Matters');
    console.log('  4. Company Overview');
    console.log('  5. HBM Technology Leadership');
    console.log('  6. The Financial Turnaround');
    console.log('  7. Financial Health Check');
    console.log('  8. Technical Analysis');
    console.log('  9. Strategic Initiatives');
    console.log(' 10. Competitive Landscape');
    console.log(' 11. Investment Recommendation');
    console.log(' 12. Price Targets & Entry Strategy');
    console.log(' 13. Key Takeaways');
    console.log(' 14. Thank You');
  })
  .catch(err => {
    console.error('❌ Error creating presentation:', err);
  });



