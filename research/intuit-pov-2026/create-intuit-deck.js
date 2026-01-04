/**
 * Intuit Investment POV - PowerPoint Presentation
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
// LAYOUT CONSTANTS
// ============================================================================
const layout = {
  margin: 0.5,
  title: { x: 0.5, y: 0.5, w: 9.0, h: 0.7 },
  subtitle: { x: 0.5, y: 1.0, w: 9.0, h: 0.3 },
  content: { x: 0.5, y: 1.4, w: 9.0, h: 3.7 },
  footer: { x: 0.5, y: 5.1, w: 9.0, h: 0.4 },
  iBeam: { x: 0, y: 0, w: 0.15, h: '100%' },
  centerTitle: { x: 0.5, y: 2.0, w: 9.0, h: 1.2 },
  centerSubtitle: { x: 0.5, y: 3.3, w: 9.0, h: 0.6 }
};

// ============================================================================
// CREATE PRESENTATION
// ============================================================================
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
pptx.author = 'Intuit Investment Research';
pptx.title = 'Intuit Investment Point of View';
pptx.subject = 'INTU Stock Analysis - January 2026';
pptx.company = 'Intuit';

// ============================================================================
// SLIDE 1: TITLE SLIDE
// ============================================================================
let slide = pptx.addSlide();
slide.background = { color: intuit.superBlue };

slide.addText('Intuit Investment POV', {
  x: 0.5, y: 2.0, w: 9.0, h: 1.2,
  fontSize: 54, fontFace: 'Avenir Next', bold: true,
  color: intuit.white, align: 'center'
});

slide.addText('Strategic Analysis | NASDAQ: INTU', {
  x: 0.5, y: 3.3, w: 9.0, h: 0.5,
  fontSize: 24, fontFace: 'Avenir Next',
  color: intuit.iceBlue, align: 'center'
});

slide.addText('January 2026', {
  x: 0.5, y: 4.0, w: 9.0, h: 0.4,
  fontSize: 18, fontFace: 'Avenir Next',
  color: intuit.lightBlue, align: 'center'
});

// Footer with Intuit mission
slide.addText('Power Prosperity Around the World', {
  x: 0.5, y: 5.0, w: 9.0, h: 0.3,
  fontSize: 14, fontFace: 'Avenir Next', italic: true,
  color: intuit.paleBlue, align: 'center'
});

// ============================================================================
// SLIDE 2: EXECUTIVE SUMMARY
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };

// I-beam accent
slide.addShape('rect', {
  x: 0, y: 0, w: 0.15, h: '100%',
  fill: { color: intuit.superBlue }
});

// Title
slide.addText('Executive Summary', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight, valign: 'top'
});

// Content
const execSummary = [
  { text: 'Intuit is a best-in-class franchise ', options: { bold: true, color: intuit.gray900 } },
  { text: 'with a powerful ecosystem built around TurboTax, QuickBooks, Credit Karma, and Mailchimp.\n\n', options: { color: intuit.gray700 } },
  { text: 'FY2025 Performance: ', options: { bold: true, color: intuit.superBlue } },
  { text: '$18.83B revenue (+15.6% YoY), $3.87B earnings (+30.6% YoY)\n\n', options: { color: intuit.gray700 } },
  { text: 'Investment Thesis: ', options: { bold: true, color: intuit.superBlue } },
  { text: 'Successfully transformed from desktop software to AI-powered platform company. Five new AI agents launched November 2025.\n\n', options: { color: intuit.gray700 } },
  { text: 'Current Opportunity: ', options: { bold: true, color: intuit.superBlue } },
  { text: 'Stock pullback to $629 (RSI: 28.79 oversold) creates attractive entry point. Analyst target: $812 (+29%).', options: { color: intuit.gray700 } }
];

slide.addText(execSummary, {
  x: 0.5, y: 1.4, w: 9.0, h: 3.5,
  fontSize: 16, fontFace: 'Avenir Next',
  color: intuit.gray700, valign: 'top'
});

// ============================================================================
// SLIDE 3: COMPANY OVERVIEW
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
    { text: '1983', options: { color: intuit.gray700 } },
    { text: 'Revenue (FY25)', options: { bold: true, color: intuit.superBlue } },
    { text: '$18.83B', options: { color: intuit.gray700 } }
  ],
  [
    { text: 'Headquarters', options: { bold: true, color: intuit.superBlue } },
    { text: 'Mountain View, CA', options: { color: intuit.gray700 } },
    { text: 'Net Income', options: { bold: true, color: intuit.superBlue } },
    { text: '$3.87B', options: { color: intuit.gray700 } }
  ],
  [
    { text: 'CEO', options: { bold: true, color: intuit.superBlue } },
    { text: 'Sasan Goodarzi', options: { color: intuit.gray700 } },
    { text: 'Market Cap', options: { bold: true, color: intuit.superBlue } },
    { text: '$175B', options: { color: intuit.gray700 } }
  ],
  [
    { text: 'Employees', options: { bold: true, color: intuit.superBlue } },
    { text: '~18,200', options: { color: intuit.gray700 } },
    { text: 'Stock Price', options: { bold: true, color: intuit.superBlue } },
    { text: '$629.46', options: { color: intuit.gray700 } }
  ]
];

slide.addTable(statsRows, {
  x: 0.5, y: 1.4, w: 9.0, h: 2.0,
  fontSize: 14, fontFace: 'Avenir Next',
  color: intuit.gray700,
  border: { type: 'solid', pt: 0.5, color: intuit.gray300 },
  fill: { color: intuit.paleBlue },
  align: 'left',
  valign: 'middle',
  colW: [1.8, 2.7, 1.8, 2.7]
});

// Products
slide.addText('Core Products', {
  x: 0.5, y: 3.6, w: 9.0, h: 0.4,
  fontSize: 18, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

const products = [
  '• TurboTax  –  Consumer & business tax preparation',
  '• QuickBooks  –  SMB accounting, payroll, payments',
  '• Credit Karma  –  Credit monitoring & financial products',
  '• Mailchimp  –  Email marketing & automation'
];

slide.addText(products.join('\n'), {
  x: 0.5, y: 4.0, w: 9.0, h: 1.2,
  fontSize: 14, fontFace: 'Avenir Next',
  color: intuit.gray700
});

// ============================================================================
// SLIDE 4: ECOSYSTEM MOAT
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: intuit.midnight };

slide.addShape('rect', {
  x: 0, y: 0, w: 0.15, h: '100%',
  fill: { color: intuit.superBlue }
});

slide.addText('The Ecosystem Moat', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.white
});

// Ecosystem description
const ecosystemText = [
  { text: 'Intuit has built what few software companies achieve: ', options: { color: intuit.lightBlue } },
  { text: 'a self-reinforcing ecosystem', options: { bold: true, color: intuit.white } },
  { text: ' that creates massive switching costs.\n\n', options: { color: intuit.lightBlue } },
  { text: '• QuickBooks ', options: { bold: true, color: intuit.skyBlue } },
  { text: 'captures SMB financial data\n', options: { color: intuit.lightBlue } },
  { text: '• Mailchimp ', options: { bold: true, color: intuit.skyBlue } },
  { text: 'handles customer acquisition\n', options: { color: intuit.lightBlue } },
  { text: '• Credit Karma ', options: { bold: true, color: intuit.skyBlue } },
  { text: 'provides personal finance insights\n', options: { color: intuit.lightBlue } },
  { text: '• TurboTax ', options: { bold: true, color: intuit.skyBlue } },
  { text: 'simplifies taxes using data from all sources\n\n', options: { color: intuit.lightBlue } },
  { text: 'Result: ', options: { bold: true, color: intuit.coral } },
  { text: '39+ million SMB customers with high retention', options: { color: intuit.white } }
];

slide.addText(ecosystemText, {
  x: 0.5, y: 1.4, w: 9.0, h: 3.5,
  fontSize: 18, fontFace: 'Avenir Next',
  valign: 'top'
});

// ============================================================================
// SLIDE 5: AI STRATEGY
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };

slide.addShape('rect', {
  x: 0, y: 0, w: 0.15, h: '100%',
  fill: { color: intuit.superBlue }
});

slide.addText('AI: The Next Growth Engine', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

slide.addText('November 2025: Intuit launched 5 new AI agents', {
  x: 0.5, y: 1.2, w: 9.0, h: 0.4,
  fontSize: 20, fontFace: 'Avenir Next', bold: true,
  color: intuit.superBlue
});

// AI Agents Table
const aiAgents = [
  [
    { text: 'AI Capability', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } },
    { text: 'Business Impact', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } }
  ],
  [
    { text: 'Automated Bookkeeping', options: { fill: { color: intuit.paleBlue } } },
    { text: 'Real-time categorization, reduces manual entry by 80%', options: { fill: { color: intuit.paleBlue } } }
  ],
  [
    { text: 'Financial Summaries', options: { fill: { color: intuit.white } } },
    { text: 'Instant CFO-level insights for SMBs', options: { fill: { color: intuit.white } } }
  ],
  [
    { text: 'Lead Generation', options: { fill: { color: intuit.paleBlue } } },
    { text: 'Smarter marketing with predictive targeting', options: { fill: { color: intuit.paleBlue } } }
  ],
  [
    { text: 'Project Management', options: { fill: { color: intuit.white } } },
    { text: 'Workflow automation for service businesses', options: { fill: { color: intuit.white } } }
  ],
  [
    { text: 'Intelligent Support', options: { fill: { color: intuit.paleBlue } } },
    { text: 'AI-powered customer assistance 24/7', options: { fill: { color: intuit.paleBlue } } }
  ]
];

slide.addTable(aiAgents, {
  x: 0.5, y: 1.7, w: 9.0, h: 2.5,
  fontSize: 14, fontFace: 'Avenir Next',
  color: intuit.gray700,
  border: { type: 'solid', pt: 0.5, color: intuit.gray300 },
  align: 'left',
  valign: 'middle',
  colW: [3.5, 5.5]
});

slide.addText('This is Intuit positioning itself as the AI-first financial operating system for SMBs', {
  x: 0.5, y: 4.4, w: 9.0, h: 0.5,
  fontSize: 16, fontFace: 'Avenir Next', italic: true,
  color: intuit.navy
});

// ============================================================================
// SLIDE 6: FINANCIAL PERFORMANCE
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };

slide.addShape('rect', {
  x: 0, y: 0, w: 0.15, h: '100%',
  fill: { color: intuit.superBlue }
});

slide.addText('Financial Performance (FY2025)', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

// Key metrics in big numbers
const metrics = [
  { label: 'Revenue', value: '$18.83B', growth: '+15.6%' },
  { label: 'Net Income', value: '$3.87B', growth: '+30.6%' },
  { label: 'Op Cash Flow', value: '$6.21B', growth: '+27.1%' }
];

metrics.forEach((metric, i) => {
  const x = 0.5 + (i * 3.0);
  
  // Big number
  slide.addText(metric.value, {
    x: x, y: 1.5, w: 2.8, h: 0.8,
    fontSize: 40, fontFace: 'Avenir Next', bold: true,
    color: intuit.superBlue, align: 'center'
  });
  
  // Label
  slide.addText(metric.label, {
    x: x, y: 2.3, w: 2.8, h: 0.4,
    fontSize: 16, fontFace: 'Avenir Next',
    color: intuit.gray700, align: 'center'
  });
  
  // Growth
  slide.addText(metric.growth + ' YoY', {
    x: x, y: 2.7, w: 2.8, h: 0.3,
    fontSize: 14, fontFace: 'Avenir Next', bold: true,
    color: intuit.forestGreen, align: 'center'
  });
});

// Ratios table
slide.addText('Key Ratios', {
  x: 0.5, y: 3.2, w: 9.0, h: 0.4,
  fontSize: 18, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

const ratioRows = [
  [
    { text: 'P/E Ratio', options: { bold: true } },
    { text: '43.29x' },
    { text: 'ROE', options: { bold: true } },
    { text: '19.6%' },
    { text: 'Debt/Equity', options: { bold: true } },
    { text: '0.34' }
  ],
  [
    { text: 'P/Sales', options: { bold: true } },
    { text: '11.67x' },
    { text: 'ROA', options: { bold: true } },
    { text: '10.5%' },
    { text: 'Current Ratio', options: { bold: true } },
    { text: '1.36' }
  ]
];

slide.addTable(ratioRows, {
  x: 0.5, y: 3.6, w: 9.0, h: 1.0,
  fontSize: 13, fontFace: 'Avenir Next',
  color: intuit.gray700,
  border: { type: 'solid', pt: 0.5, color: intuit.gray300 },
  fill: { color: intuit.paleBlue },
  align: 'center',
  valign: 'middle',
  colW: [1.5, 1.5, 1.5, 1.5, 1.5, 1.5]
});

// ============================================================================
// SLIDE 7: TECHNICAL ANALYSIS
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

// Current price box
slide.addShape('rect', {
  x: 0.5, y: 1.3, w: 3.0, h: 1.5,
  fill: { color: intuit.paleBlue },
  line: { color: intuit.superBlue, pt: 2 }
});

slide.addText('$629.46', {
  x: 0.5, y: 1.4, w: 3.0, h: 0.7,
  fontSize: 32, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight, align: 'center'
});

slide.addText('Current Price\nRSI: 28.79 (Oversold)', {
  x: 0.5, y: 2.1, w: 3.0, h: 0.6,
  fontSize: 12, fontFace: 'Avenir Next',
  color: intuit.gray700, align: 'center'
});

// Technical metrics
const techMetrics = [
  ['Indicator', 'Value', 'Signal'],
  ['SMA 50', '$659.87', 'Below'],
  ['SMA 200', '$682.48', 'Below'],
  ['RSI (14)', '28.79', 'Oversold ↓'],
  ['MACD', '-2.80', 'Bearish'],
  ['52W High', '$813.70', '-23%']
];

slide.addTable(techMetrics, {
  x: 3.8, y: 1.3, w: 5.7, h: 2.5,
  fontSize: 13, fontFace: 'Avenir Next',
  color: intuit.gray700,
  border: { type: 'solid', pt: 0.5, color: intuit.gray300 },
  align: 'center',
  valign: 'middle',
  colW: [2.0, 1.8, 1.9],
  rowH: [0.4, 0.4, 0.4, 0.4, 0.4, 0.4]
});

// Support/Resistance
slide.addText('Key Levels', {
  x: 0.5, y: 3.9, w: 9.0, h: 0.4,
  fontSize: 16, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

slide.addText([
  { text: 'Support: ', options: { bold: true, color: intuit.forestGreen } },
  { text: '$629 → $602 → $555    ', options: { color: intuit.gray700 } },
  { text: 'Resistance: ', options: { bold: true, color: intuit.coral } },
  { text: '$660 → $682 → $706 → $814', options: { color: intuit.gray700 } }
], {
  x: 0.5, y: 4.3, w: 9.0, h: 0.4,
  fontSize: 14, fontFace: 'Avenir Next'
});

// ============================================================================
// SLIDE 8: COMPETITIVE LANDSCAPE
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

// Two columns
// Advantages
slide.addText('Competitive Advantages', {
  x: 0.5, y: 1.3, w: 4.2, h: 0.4,
  fontSize: 18, fontFace: 'Avenir Next', bold: true,
  color: intuit.forestGreen
});

const advantages = [
  '✓ Brand recognition (TurboTax, QuickBooks)',
  '✓ Unmatched transaction data for AI',
  '✓ Ecosystem lock-in effects',
  '✓ 39M+ SMB customer base',
  '✓ Trust in financial data handling'
];

slide.addText(advantages.join('\n'), {
  x: 0.5, y: 1.7, w: 4.2, h: 2.0,
  fontSize: 13, fontFace: 'Avenir Next',
  color: intuit.gray700, valign: 'top'
});

// Risks
slide.addText('Key Risks to Monitor', {
  x: 5.0, y: 1.3, w: 4.5, h: 0.4,
  fontSize: 18, fontFace: 'Avenir Next', bold: true,
  color: intuit.coral
});

const risks = [
  '⚠ IRS Free File expansion pressure',
  '⚠ Xero gaining share internationally',
  '⚠ AI disruptors with fresh approach',
  '⚠ Economic sensitivity (SMB health)',
  '⚠ Premium valuation vulnerability'
];

slide.addText(risks.join('\n'), {
  x: 5.0, y: 1.7, w: 4.5, h: 2.0,
  fontSize: 13, fontFace: 'Avenir Next',
  color: intuit.gray700, valign: 'top'
});

// Competitors table
const competitorRows = [
  [
    { text: 'Competitor', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } },
    { text: 'Market', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } },
    { text: 'Threat', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } }
  ],
  ['H&R Block', 'Tax Preparation', 'Medium'],
  ['Xero', 'SMB Accounting', 'Medium'],
  ['FreshBooks', 'SMB Invoicing', 'Low'],
  ['IRS Direct File', 'Free Tax Filing', 'Medium']
];

slide.addTable(competitorRows, {
  x: 0.5, y: 3.8, w: 9.0, h: 1.5,
  fontSize: 12, fontFace: 'Avenir Next',
  color: intuit.gray700,
  border: { type: 'solid', pt: 0.5, color: intuit.gray300 },
  align: 'center',
  valign: 'middle',
  colW: [3.0, 3.0, 3.0]
});

// ============================================================================
// SLIDE 9: INVESTMENT RECOMMENDATION
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: intuit.superBlue };

slide.addText('Investment Recommendation', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.white
});

// Big recommendation
slide.addShape('rect', {
  x: 0.5, y: 1.3, w: 9.0, h: 1.2,
  fill: { color: intuit.white },
  shadow: { type: 'outer', blur: 8, offset: 4, angle: 45, opacity: 0.2 }
});

slide.addText('BUY ON WEAKNESS', {
  x: 0.5, y: 1.4, w: 9.0, h: 0.8,
  fontSize: 44, fontFace: 'Avenir Next', bold: true,
  color: intuit.forestGreen, align: 'center', valign: 'middle'
});

slide.addText('Analyst Consensus Target: $812 (+29% upside)', {
  x: 0.5, y: 2.2, w: 9.0, h: 0.3,
  fontSize: 14, fontFace: 'Avenir Next',
  color: intuit.gray700, align: 'center'
});

// Rationale
const rationale = [
  { text: 'Quality Company\n', options: { bold: true, color: intuit.white, fontSize: 16 } },
  { text: 'Best-in-class franchise with durable competitive advantages\n\n', options: { color: intuit.lightBlue, fontSize: 14 } },
  { text: 'Growth Engine\n', options: { bold: true, color: intuit.white, fontSize: 16 } },
  { text: 'AI agents represent significant new monetization lever\n\n', options: { color: intuit.lightBlue, fontSize: 14 } },
  { text: 'Technical Setup\n', options: { bold: true, color: intuit.white, fontSize: 16 } },
  { text: 'Oversold conditions (RSI: 28.79) suggest near-term bounce\n\n', options: { color: intuit.lightBlue, fontSize: 14 } },
  { text: 'Valuation\n', options: { bold: true, color: intuit.white, fontSize: 16 } },
  { text: '23% pullback from highs makes entry more attractive', options: { color: intuit.lightBlue, fontSize: 14 } }
];

slide.addText(rationale, {
  x: 0.5, y: 2.7, w: 9.0, h: 2.5,
  fontFace: 'Avenir Next',
  valign: 'top'
});

// ============================================================================
// SLIDE 10: PRICE TARGETS
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

// Price targets
const targets = [
  { scenario: 'Bull Case', price: '$800', upside: '+27%', color: intuit.forestGreen },
  { scenario: 'Base Case', price: '$750', upside: '+19%', color: intuit.superBlue },
  { scenario: 'Bear Case', price: '$550', upside: '-13%', color: intuit.coral }
];

targets.forEach((target, i) => {
  const x = 0.5 + (i * 3.0);
  
  slide.addShape('rect', {
    x: x, y: 1.4, w: 2.8, h: 1.4,
    fill: { color: intuit.paleBlue },
    line: { color: target.color, pt: 3 }
  });
  
  slide.addText(target.scenario, {
    x: x, y: 1.5, w: 2.8, h: 0.3,
    fontSize: 14, fontFace: 'Avenir Next', bold: true,
    color: intuit.gray700, align: 'center'
  });
  
  slide.addText(target.price, {
    x: x, y: 1.8, w: 2.8, h: 0.6,
    fontSize: 32, fontFace: 'Avenir Next', bold: true,
    color: target.color, align: 'center'
  });
  
  slide.addText(target.upside, {
    x: x, y: 2.4, w: 2.8, h: 0.3,
    fontSize: 14, fontFace: 'Avenir Next',
    color: intuit.gray700, align: 'center'
  });
});

// Entry strategy
slide.addText('Entry Strategy', {
  x: 0.5, y: 3.1, w: 9.0, h: 0.4,
  fontSize: 18, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

const entryStrategy = [
  { text: 'Immediate Entry: ', options: { bold: true, color: intuit.superBlue } },
  { text: 'Current levels ($629) represent reasonable entry point\n', options: { color: intuit.gray700 } },
  { text: 'Staged Entry: ', options: { bold: true, color: intuit.superBlue } },
  { text: 'Accumulate on further weakness toward $600\n', options: { color: intuit.gray700 } },
  { text: 'Technical Entry: ', options: { bold: true, color: intuit.superBlue } },
  { text: 'Wait for RSI to turn higher from oversold conditions\n', options: { color: intuit.gray700 } },
  { text: 'Stop Loss: ', options: { bold: true, color: intuit.coral } },
  { text: 'Below $520 (prior major support)', options: { color: intuit.gray700 } }
];

slide.addText(entryStrategy, {
  x: 0.5, y: 3.5, w: 9.0, h: 1.5,
  fontSize: 14, fontFace: 'Avenir Next',
  valign: 'top'
});

// ============================================================================
// SLIDE 11: KEY TAKEAWAYS
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
  { icon: '✓', text: 'Strong moat from ecosystem effects and data advantages' },
  { icon: '✓', text: 'Growth runway through AI, mid-market expansion, international' },
  { icon: '✓', text: 'Solid financials: 15.6% revenue growth, 30.6% earnings growth' },
  { icon: '✓', text: 'Capable management executing on multi-product strategy' },
  { icon: '↓', text: 'Technical pullback creates better entry valuation' }
];

takeaways.forEach((item, i) => {
  slide.addText([
    { text: item.icon + '  ', options: { color: intuit.skyBlue, fontSize: 20, bold: true } },
    { text: item.text, options: { color: intuit.lightBlue, fontSize: 18 } }
  ], {
    x: 0.5, y: 1.5 + (i * 0.7), w: 9.0, h: 0.6,
    fontFace: 'Avenir Next', valign: 'middle'
  });
});

// Bottom line
slide.addShape('rect', {
  x: 0.5, y: 4.3, w: 9.0, h: 1.0,
  fill: { color: intuit.superBlue }
});

slide.addText('Intuit is not cheap, but quality rarely is. For AI-powered financial services exposure, INTU remains one of the best franchises available.', {
  x: 0.7, y: 4.4, w: 8.6, h: 0.8,
  fontSize: 14, fontFace: 'Avenir Next', italic: true,
  color: intuit.white, align: 'center', valign: 'middle'
});

// ============================================================================
// SLIDE 12: CLOSING
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: intuit.superBlue };

slide.addText('Thank You', {
  x: 0.5, y: 2.0, w: 9.0, h: 1.0,
  fontSize: 54, fontFace: 'Avenir Next', bold: true,
  color: intuit.white, align: 'center'
});

slide.addText('Intuit Investment Point of View | January 2026', {
  x: 0.5, y: 3.2, w: 9.0, h: 0.5,
  fontSize: 18, fontFace: 'Avenir Next',
  color: intuit.lightBlue, align: 'center'
});

slide.addText('Power Prosperity Around the World', {
  x: 0.5, y: 4.8, w: 9.0, h: 0.4,
  fontSize: 14, fontFace: 'Avenir Next', italic: true,
  color: intuit.paleBlue, align: 'center'
});

// ============================================================================
// SAVE PRESENTATION
// ============================================================================
const outputPath = '/Users/snandwani2/personal/research/intuit-pov-2026/Intuit-Investment-POV-Jan2026.pptx';
pptx.writeFile({ fileName: outputPath })
  .then(() => {
    console.log('✅ Presentation created successfully!');
    console.log(`📁 Output: ${outputPath}`);
    console.log('');
    console.log('Slides created:');
    console.log('  1. Title Slide');
    console.log('  2. Executive Summary');
    console.log('  3. Company Overview');
    console.log('  4. Ecosystem Moat');
    console.log('  5. AI Strategy');
    console.log('  6. Financial Performance');
    console.log('  7. Technical Analysis');
    console.log('  8. Competitive Landscape');
    console.log('  9. Investment Recommendation');
    console.log(' 10. Price Targets & Entry Strategy');
    console.log(' 11. Key Takeaways');
    console.log(' 12. Thank You');
  })
  .catch(err => {
    console.error('❌ Error creating presentation:', err);
  });


