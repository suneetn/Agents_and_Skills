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
  green: '2ECC71',
  amber: 'F5A623',
  gold: 'FFCC4D',
  gray900: '1A1A1A',
  gray700: '4A4A4A',
  gray500: '8C8C8C',
  gray300: 'D4D4D4',
  gray100: 'F5F5F5'
};

// Layout constants
const layout = {
  margin: 0.5,
  title: { x: 0.5, y: 0.5, w: 9.0, h: 0.7 },
  content: { x: 0.5, y: 1.4, w: 9.0, h: 3.7 },
  iBeam: { x: 0, y: 0, w: 0.15, h: '100%' },
  centerTitle: { x: 0.5, y: 2.0, w: 9.0, h: 1.2 },
  centerSubtitle: { x: 0.5, y: 3.3, w: 9.0, h: 0.6 }
};

// Create presentation
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
pptx.author = 'Research Team';
pptx.title = 'Playing the AI Tidal Wave: Investment Strategies';
pptx.subject = 'AI Investment Research';

// Helper function to add I-beam accent
function addIBeam(slide, color = intuit.superBlue) {
  slide.addShape('rect', {
    x: 0, y: 0, w: 0.15, h: '100%',
    fill: { color: color }
  });
}

// Helper function for content slides
function addContentSlide(title, bullets, options = {}) {
  const slide = pptx.addSlide();
  slide.background = { color: options.bgColor || intuit.white };
  
  if (options.iBeam !== false) {
    addIBeam(slide, options.iBeamColor || intuit.superBlue);
  }
  
  slide.addText(title, {
    x: 0.5, y: 0.5, w: 9.0, h: 0.7,
    fontSize: 36, fontFace: 'Avenir Next', bold: true,
    color: intuit.midnight, valign: 'top'
  });
  
  slide.addText(bullets, {
    x: 0.5, y: 1.4, w: 9.0, h: 3.7,
    fontSize: 18, fontFace: 'Avenir Next',
    color: intuit.gray700, valign: 'top',
    bullet: options.bullet !== false
  });
  
  return slide;
}

// Helper function for section dividers
function addSectionSlide(title, subtitle = '') {
  const slide = pptx.addSlide();
  slide.background = { color: intuit.midnight };
  addIBeam(slide);
  
  slide.addText(title, {
    x: 0.5, y: 2.0, w: 8.5, h: 1.0,
    fontSize: 44, fontFace: 'Avenir Next', bold: true,
    color: intuit.white
  });
  
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.5, y: 3.1, w: 8.5, h: 0.6,
      fontSize: 24, fontFace: 'Avenir Next',
      color: intuit.lightBlue
    });
  }
  
  return slide;
}

// ============================================
// SLIDE 1: Title Slide
// ============================================
let slide = pptx.addSlide();
slide.background = { color: intuit.superBlue };

slide.addText('Playing the AI Tidal Wave', {
  x: 0.5, y: 2.0, w: 9.0, h: 1.0,
  fontSize: 54, fontFace: 'Avenir Next', bold: true,
  color: intuit.white, align: 'center'
});

slide.addText('Investment Strategies for the AI Revolution', {
  x: 0.5, y: 3.2, w: 9.0, h: 0.5,
  fontSize: 28, fontFace: 'Avenir Next',
  color: intuit.iceBlue, align: 'center'
});

slide.addText('January 2026 | Research Report', {
  x: 0.5, y: 4.5, w: 9.0, h: 0.4,
  fontSize: 18, fontFace: 'Avenir Next',
  color: intuit.lightBlue, align: 'center'
});

// ============================================
// SLIDE 2: Executive Summary
// ============================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };
addIBeam(slide);

slide.addText('Executive Summary', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

// Big number callout
slide.addText('36%', {
  x: 0.5, y: 1.3, w: 2.5, h: 1.0,
  fontSize: 72, fontFace: 'Avenir Next', bold: true,
  color: intuit.superBlue, align: 'center'
});

slide.addText('Projected Annual AI Growth\n(Next 8 Years)', {
  x: 0.5, y: 2.3, w: 2.5, h: 0.6,
  fontSize: 14, fontFace: 'Avenir Next',
  color: intuit.gray700, align: 'center'
});

// Key points
const summaryPoints = [
  { text: 'Multiple entry points across the AI value chain', options: { bullet: { code: '25CF', color: intuit.superBlue } } },
  { text: 'Semiconductors → Infrastructure → Software & Services', options: { bullet: { code: '25CF', color: intuit.superBlue } } },
  { text: 'ETFs provide diversified exposure with lower risk', options: { bullet: { code: '25CF', color: intuit.superBlue } } },
  { text: '"Picks and shovels" approach offers compelling risk/reward', options: { bullet: { code: '25CF', color: intuit.superBlue } } },
  { text: 'Power utilities are an underappreciated AI play', options: { bullet: { code: '25CF', color: intuit.superBlue } } }
];

slide.addText(summaryPoints, {
  x: 3.2, y: 1.4, w: 6.3, h: 3.5,
  fontSize: 20, fontFace: 'Avenir Next',
  color: intuit.gray900, valign: 'top'
});

// ============================================
// SLIDE 3: The AI Investment Landscape (Section)
// ============================================
addSectionSlide('The AI Investment Landscape', 'Understanding the AI Value Chain');

// ============================================
// SLIDE 4: AI Growth Cycle
// ============================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };
addIBeam(slide);

slide.addText('The AI Growth Cycle', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

// Timeline visualization
const phases = [
  { name: 'Semiconductors', status: 'Mature + Growing', color: intuit.forestGreen, x: 0.5 },
  { name: 'Infrastructure', status: 'Accelerating Now', color: intuit.superBlue, x: 3.5 },
  { name: 'Software & Services', status: 'Early Innings', color: intuit.amber, x: 6.5 }
];

phases.forEach((phase, i) => {
  // Phase box
  slide.addShape('rect', {
    x: phase.x, y: 1.5, w: 2.8, h: 1.8,
    fill: { color: phase.color },
    line: { color: phase.color }
  });
  
  slide.addText(phase.name, {
    x: phase.x, y: 1.7, w: 2.8, h: 0.5,
    fontSize: 18, fontFace: 'Avenir Next', bold: true,
    color: intuit.white, align: 'center'
  });
  
  slide.addText(phase.status, {
    x: phase.x, y: 2.4, w: 2.8, h: 0.5,
    fontSize: 14, fontFace: 'Avenir Next',
    color: intuit.white, align: 'center'
  });
  
  // Arrow between boxes
  if (i < phases.length - 1) {
    slide.addText('→', {
      x: phase.x + 2.8, y: 2.0, w: 0.7, h: 0.5,
      fontSize: 32, fontFace: 'Avenir Next', bold: true,
      color: intuit.gray500, align: 'center'
    });
  }
});

// Examples under each
const examples = [
  { text: 'NVDA, AMD, AVGO, TSM', x: 0.5 },
  { text: 'Data Centers, Power, Networking', x: 3.5 },
  { text: 'PLTR, CRM, NOW, AI Apps', x: 6.5 }
];

examples.forEach(ex => {
  slide.addText(ex.text, {
    x: ex.x, y: 3.5, w: 2.8, h: 0.5,
    fontSize: 12, fontFace: 'Avenir Next',
    color: intuit.gray700, align: 'center'
  });
});

// Key insight box
slide.addShape('rect', {
  x: 0.5, y: 4.2, w: 9.0, h: 0.8,
  fill: { color: intuit.paleBlue },
  line: { color: intuit.iceBlue }
});

slide.addText('💡 Key Insight: We\'re currently in the infrastructure phase, with software/services just beginning', {
  x: 0.7, y: 4.35, w: 8.6, h: 0.5,
  fontSize: 16, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight, align: 'center'
});

// ============================================
// SLIDE 5: Investment Approaches (Section)
// ============================================
addSectionSlide('Investment Approaches', 'Stocks, ETFs, and Strategic Frameworks');

// ============================================
// SLIDE 6: Top Individual Stocks - Hardware
// ============================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };
addIBeam(slide);

slide.addText('AI Hardware Leaders', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

slide.addText('Tier 1: The "Shovels" of the AI Gold Rush', {
  x: 0.5, y: 1.1, w: 9.0, h: 0.3,
  fontSize: 18, fontFace: 'Avenir Next',
  color: intuit.superBlue
});

// Table for hardware stocks
const hardwareTable = [
  [
    { text: 'Stock', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } },
    { text: 'Ticker', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } },
    { text: 'Price', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } },
    { text: '12M Upside', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } },
    { text: 'Key Thesis', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } }
  ],
  ['NVIDIA', 'NVDA', '$188.85', '+23%', '92% GPU market share, Blackwell sold out'],
  ['AMD', 'AMD', '~$120', '+48%', 'Growing alternative, MI350/MI400 chips'],
  ['Broadcom', 'AVGO', '~$175', '+15%', 'AI infrastructure, custom chips'],
  ['TSMC', 'TSM', '~$175', '+12%', 'Foundry dominance, makes chips for all'],
  ['ASML', 'ASML', '~$700', '+24%', 'Only maker of advanced lithography']
];

slide.addTable(hardwareTable, {
  x: 0.5, y: 1.5, w: 9.0, h: 3.0,
  fontFace: 'Avenir Next',
  fontSize: 12,
  color: intuit.gray900,
  border: { pt: 0.5, color: intuit.gray300 },
  align: 'left',
  valign: 'middle',
  colW: [1.3, 0.8, 1.0, 1.0, 4.9]
});

// ============================================
// SLIDE 7: Top Stocks - Platforms & Software
// ============================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };
addIBeam(slide);

slide.addText('AI Platforms & Software', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

// Two column layout
// Left column - Platform Giants
slide.addText('Cloud & Platform Giants', {
  x: 0.5, y: 1.2, w: 4.2, h: 0.4,
  fontSize: 18, fontFace: 'Avenir Next', bold: true,
  color: intuit.superBlue
});

const platformStocks = [
  { text: 'Microsoft (MSFT) - Azure AI, OpenAI partnership', options: { bullet: { code: '25CF', color: intuit.superBlue } } },
  { text: 'Alphabet (GOOGL) - Gemini, Cloud AI, P/E: 23', options: { bullet: { code: '25CF', color: intuit.superBlue } } },
  { text: 'Amazon (AMZN) - AWS Bedrock leader', options: { bullet: { code: '25CF', color: intuit.superBlue } } },
  { text: 'Meta (META) - AI ads, Llama models', options: { bullet: { code: '25CF', color: intuit.superBlue } } }
];

slide.addText(platformStocks, {
  x: 0.5, y: 1.6, w: 4.2, h: 2.0,
  fontSize: 14, fontFace: 'Avenir Next',
  color: intuit.gray900
});

// Right column - Software
slide.addText('AI Software Leaders', {
  x: 5.0, y: 1.2, w: 4.5, h: 0.4,
  fontSize: 18, fontFace: 'Avenir Next', bold: true,
  color: intuit.superBlue
});

const softwareStocks = [
  { text: 'Palantir (PLTR) - +20% growth, enterprise AI', options: { bullet: { code: '25CF', color: intuit.forestGreen } } },
  { text: 'Salesforce (CRM) - Einstein AI integration', options: { bullet: { code: '25CF', color: intuit.forestGreen } } },
  { text: 'ServiceNow (NOW) - AI workflow automation', options: { bullet: { code: '25CF', color: intuit.forestGreen } } },
  { text: 'Snowflake (SNOW) - AI data cloud', options: { bullet: { code: '25CF', color: intuit.forestGreen } } }
];

slide.addText(softwareStocks, {
  x: 5.0, y: 1.6, w: 4.5, h: 2.0,
  fontSize: 14, fontFace: 'Avenir Next',
  color: intuit.gray900
});

// Infrastructure callout
slide.addShape('rect', {
  x: 0.5, y: 3.8, w: 9.0, h: 1.4,
  fill: { color: intuit.paleBlue },
  line: { color: intuit.iceBlue }
});

slide.addText('🔌 Often Overlooked: Power & Infrastructure', {
  x: 0.7, y: 3.95, w: 8.6, h: 0.35,
  fontSize: 16, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

slide.addText('Vistra (VST) +45% | Constellation Energy (CEG) +40% | Arista Networks (ANET) +50% | Vertiv (VRT) +80%', {
  x: 0.7, y: 4.35, w: 8.6, h: 0.3,
  fontSize: 14, fontFace: 'Avenir Next',
  color: intuit.gray700
});

slide.addText('Nuclear utilities provide consistent, zero-emission power for AI data centers', {
  x: 0.7, y: 4.7, w: 8.6, h: 0.3,
  fontSize: 12, fontFace: 'Avenir Next', italic: true,
  color: intuit.gray500
});

// ============================================
// SLIDE 8: ETF Strategies (Section)
// ============================================
addSectionSlide('ETF Strategies', 'Diversified Exposure to AI Growth');

// ============================================
// SLIDE 9: Recommended ETF Portfolio
// ============================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };
addIBeam(slide);

slide.addText('Recommended ETF Portfolio', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

const etfTable = [
  [
    { text: 'ETF', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } },
    { text: 'Symbol', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } },
    { text: 'Weight', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } },
    { text: 'Exp. Ratio', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } },
    { text: '1Y Return', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } },
    { text: 'Focus', options: { bold: true, fill: { color: intuit.superBlue }, color: intuit.white } }
  ],
  ['VanEck Semiconductor', 'SMH', '30%', '0.35%', '+39%', 'Chip makers (NVDA 20%)'],
  ['NASDAQ 100', 'QQQ', '25%', '0.20%', '+25%', 'Tech foundation'],
  ['Roundhill Gen AI', 'CHAT', '20%', '0.75%', '+35%', 'Pure-play generative AI'],
  ['S&P 500 Momentum', 'SPMO', '15%', '0.13%', '+38%', 'Risk-adjusted winners'],
  ['Utilities (Nuclear)', 'UTES', '10%', '0.49%', '+45%', 'AI power infrastructure']
];

slide.addTable(etfTable, {
  x: 0.5, y: 1.3, w: 9.0, h: 2.5,
  fontFace: 'Avenir Next',
  fontSize: 12,
  color: intuit.gray900,
  border: { pt: 0.5, color: intuit.gray300 },
  align: 'center',
  valign: 'middle',
  colW: [2.0, 0.9, 0.9, 0.9, 0.9, 3.4]
});

// Visual pie chart approximation
slide.addText('Portfolio Allocation', {
  x: 0.5, y: 4.0, w: 2.5, h: 0.4,
  fontSize: 14, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

const allocations = [
  { label: 'SMH 30%', color: intuit.superBlue, x: 0.5 },
  { label: 'QQQ 25%', color: intuit.navy, x: 2.0 },
  { label: 'CHAT 20%', color: intuit.forestGreen, x: 3.5 },
  { label: 'SPMO 15%', color: intuit.amber, x: 5.0 },
  { label: 'UTES 10%', color: intuit.coral, x: 6.5 }
];

allocations.forEach(a => {
  slide.addShape('rect', {
    x: a.x, y: 4.4, w: 1.3, h: 0.3,
    fill: { color: a.color }
  });
  slide.addText(a.label, {
    x: a.x, y: 4.75, w: 1.3, h: 0.3,
    fontSize: 11, fontFace: 'Avenir Next',
    color: intuit.gray700, align: 'center'
  });
});

// ============================================
// SLIDE 10: Alternative ETFs
// ============================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };
addIBeam(slide);

slide.addText('Alternative ETF Options', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

const altEtfTable = [
  [
    { text: 'ETF', options: { bold: true, fill: { color: intuit.navy }, color: intuit.white } },
    { text: 'Symbol', options: { bold: true, fill: { color: intuit.navy }, color: intuit.white } },
    { text: 'Exp. Ratio', options: { bold: true, fill: { color: intuit.navy }, color: intuit.white } },
    { text: 'Holdings', options: { bold: true, fill: { color: intuit.navy }, color: intuit.white } },
    { text: 'Focus', options: { bold: true, fill: { color: intuit.navy }, color: intuit.white } }
  ],
  ['Global X AI & Tech', 'AIQ', '0.68%', '85', 'Broad AI, includes Asian tech'],
  ['ARK Autonomous Tech', 'ARKQ', '0.75%', '35', 'Robotics, autonomous vehicles'],
  ['ROBO Global', 'ROBO', '0.95%', '80+', 'Global robotics & automation'],
  ['iShares Robotics', 'IRBO', '0.47%', '100+', 'Equal-weighted exposure'],
  ['Vanguard IT Index', 'VGT', '0.10%', '350+', 'Lowest cost, broad tech'],
  ['Defiance Quantum', 'QTUM', '0.40%', '70', 'Quantum computing + AI']
];

slide.addTable(altEtfTable, {
  x: 0.5, y: 1.3, w: 9.0, h: 2.8,
  fontFace: 'Avenir Next',
  fontSize: 12,
  color: intuit.gray900,
  border: { pt: 0.5, color: intuit.gray300 },
  align: 'center',
  valign: 'middle',
  colW: [2.0, 1.0, 1.0, 1.0, 4.0]
});

// Warning about overlap
slide.addShape('rect', {
  x: 0.5, y: 4.3, w: 9.0, h: 0.8,
  fill: { color: intuit.gold },
  line: { color: intuit.amber }
});

slide.addText('⚠️ Watch for Overlap: VGT & QQQ overlap 99% - choose one, not both', {
  x: 0.7, y: 4.5, w: 8.6, h: 0.4,
  fontSize: 16, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight, align: 'center'
});

// ============================================
// SLIDE 11: Strategic Approaches (Section)
// ============================================
addSectionSlide('Strategic Approaches', 'Portfolio Frameworks by Risk Profile');

// ============================================
// SLIDE 12: Three Portfolio Strategies
// ============================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };
addIBeam(slide);

slide.addText('Portfolio Strategies by Risk Tolerance', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

// Three columns
const strategies = [
  {
    title: 'Conservative',
    subtitle: 'AI: 25-35%',
    color: intuit.forestGreen,
    items: ['40% S&P 500', '25% NASDAQ 100', '10-15% SMH', '5-10% UTES'],
    x: 0.5
  },
  {
    title: 'Moderate',
    subtitle: 'AI: 50-60%',
    color: intuit.superBlue,
    items: ['40% QQQ', '20% SMH', '15% CHAT', '15% Individual', '10% Infrastructure'],
    x: 3.5
  },
  {
    title: 'Aggressive',
    subtitle: 'AI: 80-100%',
    color: intuit.coral,
    items: ['30% SMH + NVDA', '25% CHAT + PLTR', '15% Infrastructure', '10% QTUM'],
    x: 6.5
  }
];

strategies.forEach(s => {
  // Header box
  slide.addShape('rect', {
    x: s.x, y: 1.3, w: 2.8, h: 0.9,
    fill: { color: s.color }
  });
  
  slide.addText(s.title, {
    x: s.x, y: 1.4, w: 2.8, h: 0.45,
    fontSize: 20, fontFace: 'Avenir Next', bold: true,
    color: intuit.white, align: 'center'
  });
  
  slide.addText(s.subtitle, {
    x: s.x, y: 1.85, w: 2.8, h: 0.3,
    fontSize: 14, fontFace: 'Avenir Next',
    color: intuit.white, align: 'center'
  });
  
  // Content box
  slide.addShape('rect', {
    x: s.x, y: 2.2, w: 2.8, h: 2.5,
    fill: { color: intuit.gray100 },
    line: { color: intuit.gray300 }
  });
  
  const bulletItems = s.items.map(item => ({
    text: item,
    options: { bullet: { code: '25CF', color: s.color } }
  }));
  
  slide.addText(bulletItems, {
    x: s.x + 0.1, y: 2.4, w: 2.6, h: 2.2,
    fontSize: 13, fontFace: 'Avenir Next',
    color: intuit.gray900, valign: 'top'
  });
});

// ============================================
// SLIDE 13: Risk Assessment (Section)
// ============================================
addSectionSlide('Risk Assessment', 'Understanding and Managing AI Investment Risks');

// ============================================
// SLIDE 14: Key Risks
// ============================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };
addIBeam(slide, intuit.coral);

slide.addText('Key Risks to Monitor', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

// Risk cards
const risks = [
  { icon: '📉', title: 'Valuation Risk', desc: 'NVDA P/E ~65, sector premiums leave room for pullbacks' },
  { icon: '⚔️', title: 'Competition', desc: 'AMD, Intel, custom chips from Google/Amazon challenge NVDA' },
  { icon: '⚖️', title: 'Regulatory Risk', desc: 'Government AI regulations could slow adoption' },
  { icon: '⚡', title: 'Energy Constraints', desc: 'Data center power demand may outpace supply' },
  { icon: '🎯', title: 'Concentration Risk', desc: 'Heavy NVDA weighting in many AI funds' }
];

risks.forEach((risk, i) => {
  const row = Math.floor(i / 3);
  const col = i % 3;
  const x = 0.5 + (col * 3.1);
  const y = 1.3 + (row * 1.8);
  
  slide.addShape('rect', {
    x: x, y: y, w: 2.9, h: 1.5,
    fill: { color: intuit.white },
    line: { color: intuit.coral, pt: 2 }
  });
  
  slide.addText(risk.icon + ' ' + risk.title, {
    x: x + 0.1, y: y + 0.1, w: 2.7, h: 0.4,
    fontSize: 14, fontFace: 'Avenir Next', bold: true,
    color: intuit.coral
  });
  
  slide.addText(risk.desc, {
    x: x + 0.1, y: y + 0.5, w: 2.7, h: 0.9,
    fontSize: 12, fontFace: 'Avenir Next',
    color: intuit.gray700
  });
});

// Mitigation box
slide.addShape('rect', {
  x: 0.5, y: 4.5, w: 9.0, h: 0.6,
  fill: { color: intuit.forestGreen }
});

slide.addText('✓ Mitigation: Dollar-cost average, diversify across value chain, set position limits, rebalance quarterly', {
  x: 0.7, y: 4.6, w: 8.6, h: 0.4,
  fontSize: 14, fontFace: 'Avenir Next', bold: true,
  color: intuit.white, align: 'center'
});

// ============================================
// SLIDE 15: Actionable Recommendations (Section)
// ============================================
addSectionSlide('Actionable Recommendations', 'Next Steps for Your Portfolio');

// ============================================
// SLIDE 16: Implementation Checklist
// ============================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };
addIBeam(slide, intuit.forestGreen);

slide.addText('Implementation Checklist', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

const checklist = [
  { text: '☐  Assess current portfolio for existing AI exposure', options: { bullet: false } },
  { text: '☐  Determine risk tolerance and appropriate allocation', options: { bullet: false } },
  { text: '☐  Choose between individual stocks vs. ETFs vs. hybrid', options: { bullet: false } },
  { text: '☐  Set up dollar-cost averaging schedule for new positions', options: { bullet: false } },
  { text: '☐  Plan rebalancing frequency (quarterly recommended)', options: { bullet: false } },
  { text: '☐  Monitor sector concentration and overlap', options: { bullet: false } },
  { text: '☐  Track key AI developments and adjust thesis as needed', options: { bullet: false } }
];

slide.addText(checklist, {
  x: 0.5, y: 1.3, w: 9.0, h: 3.5,
  fontSize: 20, fontFace: 'Avenir Next',
  color: intuit.gray900, valign: 'top',
  paraSpaceAfter: 14
});

// ============================================
// SLIDE 17: Conclusion
// ============================================
slide = pptx.addSlide();
slide.background = { color: intuit.midnight };
addIBeam(slide);

slide.addText('Key Takeaways', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.white
});

const takeaways = [
  { text: 'Understand the AI value chain: Chips → Infrastructure → Software', options: { bullet: { code: '25CF', color: intuit.superBlue } } },
  { text: 'Diversify across layers for balanced exposure', options: { bullet: { code: '25CF', color: intuit.superBlue } } },
  { text: 'Use ETFs for broad exposure, individual stocks for conviction', options: { bullet: { code: '25CF', color: intuit.superBlue } } },
  { text: 'Don\'t ignore "boring" infrastructure plays like utilities', options: { bullet: { code: '25CF', color: intuit.superBlue } } },
  { text: 'Manage risk through position sizing and regular rebalancing', options: { bullet: { code: '25CF', color: intuit.superBlue } } }
];

slide.addText(takeaways, {
  x: 0.5, y: 1.3, w: 9.0, h: 2.8,
  fontSize: 20, fontFace: 'Avenir Next',
  color: intuit.white, valign: 'top',
  paraSpaceAfter: 12
});

// Big callout
slide.addShape('rect', {
  x: 0.5, y: 4.2, w: 9.0, h: 0.9,
  fill: { color: intuit.superBlue }
});

slide.addText('36% projected annual AI growth = Generational investment opportunity', {
  x: 0.7, y: 4.35, w: 8.6, h: 0.6,
  fontSize: 22, fontFace: 'Avenir Next', bold: true,
  color: intuit.white, align: 'center'
});

// ============================================
// SLIDE 18: Thank You / Questions
// ============================================
slide = pptx.addSlide();
slide.background = { color: intuit.superBlue };

slide.addText('Questions?', {
  x: 0.5, y: 2.2, w: 9.0, h: 1.0,
  fontSize: 54, fontFace: 'Avenir Next', bold: true,
  color: intuit.white, align: 'center'
});

slide.addText('Research conducted January 2026', {
  x: 0.5, y: 3.5, w: 9.0, h: 0.5,
  fontSize: 18, fontFace: 'Avenir Next',
  color: intuit.iceBlue, align: 'center'
});

slide.addText('Full research document: /research/ai-investing-strategies/', {
  x: 0.5, y: 4.2, w: 9.0, h: 0.4,
  fontSize: 14, fontFace: 'Avenir Next',
  color: intuit.lightBlue, align: 'center'
});

// ============================================
// Save the presentation
// ============================================
pptx.writeFile({ fileName: 'AI-Investment-Strategies-Jan2026.pptx' })
  .then(fileName => {
    console.log(`✅ Presentation created: ${fileName}`);
  })
  .catch(err => {
    console.error('Error creating presentation:', err);
  });

