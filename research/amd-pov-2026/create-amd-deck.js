const pptxgen = require('pptxgenjs');

// Intuit Brand Colors
const intuit = {
  superBlue: '236CFF',
  midnight: '0D2644',
  navy: '1A3D5C',
  white: 'FFFFFF',
  skyBlue: '5A94FF',
  lightBlue: '8FB8FF',
  iceBlue: 'C4DBFF',
  paleBlue: 'E8F1FF',
  amdRed: 'ED1C24',
  forestGreen: '0A5C36',
  amber: 'F5A623',
  gray900: '1A1A1A',
  gray700: '4A4A4A',
  gray500: '8C8C8C',
  gray100: 'F5F5F5'
};

// Layout constants
const layout = {
  title: { x: 0.5, y: 0.5, w: 9.0, h: 0.7 },
  content: { x: 0.5, y: 1.4, w: 9.0, h: 3.7 },
  iBeam: { x: 0, y: 0, w: 0.15, h: '100%' }
};

// Create presentation
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
pptx.author = 'Intuit Investment Research';
pptx.title = 'AMD Investment POV';

// ============================================================
// SLIDE 1: Title Slide
// ============================================================
let slide1 = pptx.addSlide();
slide1.addShape('rect', { x: 0, y: 0, w: '100%', h: '100%', fill: { color: intuit.superBlue } });
slide1.addShape('rect', { x: 0, y: 4.8, w: '100%', h: 0.7, fill: { color: intuit.midnight } });

slide1.addText('Advanced Micro Devices (AMD)', {
  x: 0.5, y: 1.8, w: 9, h: 1,
  fontSize: 40, fontFace: 'Avenir Next', bold: true, color: intuit.white
});
slide1.addText('Investment Point of View', {
  x: 0.5, y: 2.7, w: 9, h: 0.6,
  fontSize: 28, fontFace: 'Avenir Next', color: intuit.iceBlue
});
slide1.addText('The Essential Alternative in AI Infrastructure', {
  x: 0.5, y: 3.4, w: 9, h: 0.5,
  fontSize: 20, fontFace: 'Avenir Next', italic: true, color: intuit.white
});
slide1.addText('January 2026 | Research Analysis', {
  x: 0.5, y: 5.0, w: 9, h: 0.4,
  fontSize: 14, fontFace: 'Avenir Next', color: intuit.lightBlue
});

// ============================================================
// SLIDE 2: Executive Summary
// ============================================================
let slide2 = pptx.addSlide();
slide2.addShape('rect', { ...layout.iBeam, fill: { color: intuit.superBlue } });
slide2.addText('Executive Summary', {
  ...layout.title, fontSize: 28, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

slide2.addText([
  { text: 'Investment Rating: ', options: { bold: true, color: intuit.midnight } },
  { text: 'BUY on Pullbacks', options: { bold: true, color: intuit.forestGreen } }
], { x: 0.5, y: 1.3, w: 9, h: 0.4, fontSize: 18, fontFace: 'Avenir Next' });

slide2.addText([
  { text: '12-Month Price Target: ', options: { bold: true } },
  { text: '$270-$300 (Current: $223) → 21-34% Upside', options: { color: intuit.gray700 } }
], { x: 0.5, y: 1.7, w: 9, h: 0.4, fontSize: 16, fontFace: 'Avenir Next', color: intuit.midnight });

const summaryBullets = [
  'OpenAI partnership: Multi-year deal for 6GW of GPUs, potential 10% stake for OpenAI',
  'Record Q3 2025: $9.2B revenue (+36% YoY), data center segment +60% YoY',
  'Analyst consensus: "Strong Buy" with $280 average price target',
  'Supply/demand dynamics: Nvidia demand exceeds supply 10:1, AMD fills the gap',
  'MI400/450 launch in 2026: Rack-scale solutions unlock hyperscaler opportunity'
];

slide2.addText(summaryBullets.map(b => ({ text: b, options: { bullet: true, paraSpaceAfter: 10 } })), {
  x: 0.5, y: 2.2, w: 9, h: 2.8, fontSize: 15, fontFace: 'Avenir Next', color: intuit.gray700, valign: 'top'
});

// ============================================================
// SLIDE 3: The Numbers
// ============================================================
let slide3 = pptx.addSlide();
slide3.addShape('rect', { ...layout.iBeam, fill: { color: intuit.superBlue } });
slide3.addText('The Numbers at a Glance', {
  ...layout.title, fontSize: 28, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

const metricsData = [
  ['Metric', 'Value', 'Context'],
  ['Stock Price', '$223.47', '+4.35% today, +43% YTD'],
  ['Market Cap', '$362.7B', '#2 in AI accelerators'],
  ['P/E Ratio', '117x', 'Premium for growth'],
  ['Revenue (Q3)', '$9.2B', 'Record (+36% YoY)'],
  ['Data Center Rev', '$4.3B', '+60% YoY (largest segment)'],
  ['Net Income Growth', '+92% YoY', 'Profitability improving']
];

slide3.addTable(metricsData, {
  x: 0.5, y: 1.3, w: 9, h: 3.2,
  fontFace: 'Avenir Next',
  fontSize: 13,
  color: intuit.gray700,
  border: { pt: 0.5, color: intuit.iceBlue },
  fill: { color: intuit.white },
  colW: [2.5, 2.5, 4],
  rowH: 0.45,
  align: 'left',
  valign: 'middle'
});

slide3.addShape('rect', { x: 0.5, y: 1.3, w: 9, h: 0.45, fill: { color: intuit.superBlue } });
slide3.addText(['Metric', 'Value', 'Context'].join('          '), {
  x: 0.5, y: 1.3, w: 9, h: 0.45, fontSize: 13, fontFace: 'Avenir Next', bold: true, color: intuit.white, valign: 'middle', margin: [0, 0, 0, 10]
});

// ============================================================
// SLIDE 4: OpenAI Partnership
// ============================================================
let slide4 = pptx.addSlide();
slide4.addShape('rect', { ...layout.iBeam, fill: { color: intuit.forestGreen } });
slide4.addText('Game-Changer: The OpenAI Partnership', {
  ...layout.title, fontSize: 26, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

slide4.addText('Deal Structure', {
  x: 0.5, y: 1.3, w: 4.2, h: 0.4, fontSize: 16, fontFace: 'Avenir Next', bold: true, color: intuit.forestGreen
});
slide4.addText('• 1 gigawatt GPUs deploying 2026\n• Scaling to 6 gigawatts total\n• OpenAI gets 160M shares at $0.01\n• Potential 10% stake worth ~$36B', {
  x: 0.5, y: 1.7, w: 4.2, h: 1.3, fontSize: 12, fontFace: 'Avenir Next', color: intuit.gray700
});

slide4.addText('Why It Matters', {
  x: 5, y: 1.3, w: 4.5, h: 0.4, fontSize: 16, fontFace: 'Avenir Next', bold: true, color: intuit.forestGreen
});
slide4.addText('• Legitimizes AMD as Tier 1 supplier\n• OpenAI diversifying from Nvidia\n• Follows $100B Nvidia deal by weeks\n• Creates competitive hedge', {
  x: 5, y: 1.7, w: 4.5, h: 1.3, fontSize: 12, fontFace: 'Avenir Next', color: intuit.gray700
});

slide4.addText('Additional Partnerships', {
  x: 0.5, y: 3.1, w: 9, h: 0.4, fontSize: 16, fontFace: 'Avenir Next', bold: true, color: intuit.forestGreen
});
slide4.addText('Oracle: 50,000 MI450 GPUs in AI supercluster by Q3 2026 | Hyperscalers actively seeking AMD as Nvidia alternative', {
  x: 0.5, y: 3.5, w: 9, h: 0.5, fontSize: 12, fontFace: 'Avenir Next', color: intuit.gray700
});

slide4.addText('"This is all about OpenAI locking in the supply chain that it needs to scale." — CNBC', {
  x: 0.5, y: 4.2, w: 9, h: 0.6, fontSize: 12, fontFace: 'Avenir Next', italic: true, color: intuit.superBlue
});

// ============================================================
// SLIDE 5: The Bull Thesis
// ============================================================
let slide5 = pptx.addSlide();
slide5.addShape('rect', { ...layout.iBeam, fill: { color: intuit.forestGreen } });
slide5.addText('Bull Thesis: "The Essential Alternative"', {
  ...layout.title, fontSize: 26, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

const bullPoints = [
  { text: 'Demand Exceeds Supply 10:1: ', detail: 'Wedbush channel checks show Nvidia demand far exceeds supply. AMD just needs to ship product.' },
  { text: 'Hyperscalers WANT AMD: ', detail: 'Microsoft, Google, Amazon uncomfortable with Nvidia monopoly. They\'re giving AMD opportunities.' },
  { text: 'MI400 Rack-Scale 2026: ', detail: 'ZT Systems acquisition enables rack-scale solutions. "1000% quarter-over-quarter growth potential."' },
  { text: 'Not Trying to Beat Nvidia: ', detail: 'AMD positioned as essential #2. Hyperscalers need two suppliers for negotiating leverage.' },
  { text: 'Gaming/Client Recovery: ', detail: 'Ryzen 9800X3D driving record client revenue. Gaming +181% YoY.' }
];

bullPoints.forEach((point, i) => {
  slide5.addText([
    { text: point.text, options: { bold: true, color: intuit.forestGreen } },
    { text: point.detail, options: { color: intuit.gray700 } }
  ], { x: 0.5, y: 1.3 + (i * 0.6), w: 9, h: 0.55, fontSize: 12, fontFace: 'Avenir Next' });
});

slide5.addText('"With this demand imbalance, it\'s not a matter of AMD having to fight for share. It\'s just: can they offer the product?" — MarketBeat', {
  x: 0.5, y: 4.3, w: 9, h: 0.5, fontSize: 11, fontFace: 'Avenir Next', italic: true, color: intuit.gray500
});

// ============================================================
// SLIDE 6: The Bear Thesis
// ============================================================
let slide6 = pptx.addSlide();
slide6.addShape('rect', { ...layout.iBeam, fill: { color: intuit.amdRed } });
slide6.addText('Bear Thesis: Nvidia\'s Shadow Looms Large', {
  ...layout.title, fontSize: 26, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

const bearPoints = [
  { text: 'Valuation vs Nvidia: ', detail: 'AMD P/E of 117x vs Nvidia 65x. DCF fair value: $193 per CFA analysis.' },
  { text: 'ROIC Struggles: ', detail: 'AMD ROIC <5% for 4 years vs Nvidia\'s 175%. Reflects #2 market position.' },
  { text: 'In-House Chips: ', detail: 'Amazon, Microsoft, Google developing internal chips. Could reduce AMD\'s "alternative" value.' },
  { text: 'Intel-Nvidia Partnership: ', detail: 'AMD flagged as business risk in quarterly filing. New competitive pressure.' },
  { text: 'Execution Risk: ', detail: 'MI400/450 launch must succeed to capture hyperscaler demand.' }
];

bearPoints.forEach((point, i) => {
  slide6.addText([
    { text: point.text, options: { bold: true, color: intuit.amdRed } },
    { text: point.detail, options: { color: intuit.gray700 } }
  ], { x: 0.5, y: 1.3 + (i * 0.6), w: 9, h: 0.55, fontSize: 12, fontFace: 'Avenir Next' });
});

slide6.addText('"Nvidia is performing much better across every single metric and trading at a lower valuation." — Parkev Tatevosian, CFA', {
  x: 0.5, y: 4.3, w: 9, h: 0.5, fontSize: 11, fontFace: 'Avenir Next', italic: true, color: intuit.gray500
});

// ============================================================
// SLIDE 7: Technical Analysis
// ============================================================
let slide7 = pptx.addSlide();
slide7.addShape('rect', { ...layout.iBeam, fill: { color: intuit.superBlue } });
slide7.addText('Technical Analysis', {
  ...layout.title, fontSize: 28, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

const technicalData = [
  ['Indicator', 'Value', 'Signal'],
  ['Price', '$223.47', '+4.35% today'],
  ['RSI (14)', '51.86', 'Neutral'],
  ['MACD', 'Bullish crossover', 'Positive'],
  ['vs SMA 50', 'Below ($227.63)', 'Consolidating'],
  ['vs SMA 200', 'Above ($163.23)', 'Long-term uptrend'],
  ['1-Year Return', '+43.37%', 'Strong momentum']
];

slide7.addTable(technicalData, {
  x: 0.5, y: 1.3, w: 5.5, h: 2.8,
  fontFace: 'Avenir Next',
  fontSize: 12,
  color: intuit.gray700,
  border: { pt: 0.5, color: intuit.iceBlue },
  fill: { color: intuit.white },
  colW: [1.8, 1.8, 1.9],
  rowH: 0.38
});

slide7.addText('Key Levels', {
  x: 6.2, y: 1.3, w: 3.3, h: 0.4, fontSize: 16, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

slide7.addText([
  { text: 'Support:\n', options: { bold: true, color: intuit.forestGreen } },
  { text: '• $219 (S1)\n• $215 (S2)\n• $163 (200 SMA)\n\n', options: { color: intuit.gray700 } },
  { text: 'Resistance:\n', options: { bold: true, color: intuit.amdRed } },
  { text: '• $227 (R1)\n• $231 (R2)\n• $267 (52-wk high)', options: { color: intuit.gray700 } }
], { x: 6.2, y: 1.7, w: 3.3, h: 2.5, fontSize: 12, fontFace: 'Avenir Next' });

slide7.addText('Overall Signal: HOLD → BUY on dips to $200-215 zone', {
  x: 0.5, y: 4.3, w: 9, h: 0.4, fontSize: 13, fontFace: 'Avenir Next', bold: true, color: intuit.superBlue
});

// ============================================================
// SLIDE 8: Scenario Analysis
// ============================================================
let slide8 = pptx.addSlide();
slide8.addShape('rect', { ...layout.iBeam, fill: { color: intuit.superBlue } });
slide8.addText('Scenario Analysis: 2026 Price Targets', {
  ...layout.title, fontSize: 28, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

// Bull box
slide8.addShape('rect', { x: 0.5, y: 1.3, w: 2.9, h: 2.8, fill: { color: 'E8F5E9' }, line: { color: intuit.forestGreen, pt: 2 } });
slide8.addText('BULL CASE', { x: 0.5, y: 1.35, w: 2.9, h: 0.4, fontSize: 14, fontFace: 'Avenir Next', bold: true, color: intuit.forestGreen, align: 'center' });
slide8.addText('$300-$350', { x: 0.5, y: 1.75, w: 2.9, h: 0.5, fontSize: 24, fontFace: 'Avenir Next', bold: true, color: intuit.forestGreen, align: 'center' });
slide8.addText('30% probability\n\n• OpenAI scales as planned\n• MI400 launch succeeds\n• Data center $8B+/qtr\n• P/E sustained 50-60x', {
  x: 0.6, y: 2.3, w: 2.7, h: 1.7, fontSize: 10, fontFace: 'Avenir Next', color: intuit.gray700
});

// Base box
slide8.addShape('rect', { x: 3.55, y: 1.3, w: 2.9, h: 2.8, fill: { color: intuit.paleBlue }, line: { color: intuit.superBlue, pt: 2 } });
slide8.addText('BASE CASE', { x: 3.55, y: 1.35, w: 2.9, h: 0.4, fontSize: 14, fontFace: 'Avenir Next', bold: true, color: intuit.superBlue, align: 'center' });
slide8.addText('$250-$280', { x: 3.55, y: 1.75, w: 2.9, h: 0.5, fontSize: 24, fontFace: 'Avenir Next', bold: true, color: intuit.superBlue, align: 'center' });
slide8.addText('50% probability\n\n• Steady share gains 15-20%\n• DC revenue +40-50% YoY\n• OpenAI $5B+ annually\n• P/E contracts to 35-45x', {
  x: 3.65, y: 2.3, w: 2.7, h: 1.7, fontSize: 10, fontFace: 'Avenir Next', color: intuit.gray700
});

// Bear box
slide8.addShape('rect', { x: 6.6, y: 1.3, w: 2.9, h: 2.8, fill: { color: 'FFEBEE' }, line: { color: intuit.amdRed, pt: 2 } });
slide8.addText('BEAR CASE', { x: 6.6, y: 1.35, w: 2.9, h: 0.4, fontSize: 14, fontFace: 'Avenir Next', bold: true, color: intuit.amdRed, align: 'center' });
slide8.addText('$150-$180', { x: 6.6, y: 1.75, w: 2.9, h: 0.5, fontSize: 24, fontFace: 'Avenir Next', bold: true, color: intuit.amdRed, align: 'center' });
slide8.addText('20% probability\n\n• MI400 launch delays\n• In-house chips dominate\n• Nvidia maintains 85%+\n• P/E compresses to 25-30x', {
  x: 6.7, y: 2.3, w: 2.7, h: 1.7, fontSize: 10, fontFace: 'Avenir Next', color: intuit.gray700
});

slide8.addText('Current price $223 offers favorable risk/reward. Analyst consensus: $280 target (25% upside).', {
  x: 0.5, y: 4.3, w: 9, h: 0.4, fontSize: 12, fontFace: 'Avenir Next', italic: true, color: intuit.gray500
});

// ============================================================
// SLIDE 9: AMD vs Nvidia
// ============================================================
let slide9 = pptx.addSlide();
slide9.addShape('rect', { ...layout.iBeam, fill: { color: intuit.superBlue } });
slide9.addText('AMD vs Nvidia: Quick Comparison', {
  ...layout.title, fontSize: 28, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

const compData = [
  ['Metric', 'AMD', 'NVDA', 'Winner'],
  ['Market Cap', '$363B', '$3.2T', 'NVDA'],
  ['P/E Ratio', '117x', '65x', 'NVDA'],
  ['Revenue Growth', '+36%', '+94%', 'NVDA'],
  ['Gross Margin', '52%', '75%', 'NVDA'],
  ['ROIC', '3%', '175%', 'NVDA'],
  ['AI Market Share', '~15%', '~80%', 'NVDA'],
  ['Analyst Upside', '25%', '15%', 'AMD']
];

slide9.addTable(compData, {
  x: 0.5, y: 1.3, w: 9, h: 2.8,
  fontFace: 'Avenir Next',
  fontSize: 12,
  color: intuit.gray700,
  border: { pt: 0.5, color: intuit.iceBlue },
  fill: { color: intuit.white },
  colW: [2.5, 2.2, 2.2, 2.1],
  rowH: 0.32
});

slide9.addText('Bottom Line: Nvidia is the superior business. AMD is the higher-risk, higher-reward bet on becoming the essential #2.', {
  x: 0.5, y: 4.2, w: 9, h: 0.5, fontSize: 13, fontFace: 'Avenir Next', bold: true, color: intuit.superBlue
});

// ============================================================
// SLIDE 10: Investment Recommendation
// ============================================================
let slide10 = pptx.addSlide();
slide10.addShape('rect', { ...layout.iBeam, fill: { color: intuit.forestGreen } });
slide10.addText('Investment Recommendation', {
  ...layout.title, fontSize: 28, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

slide10.addShape('rect', { x: 0.5, y: 1.25, w: 9, h: 0.6, fill: { color: intuit.forestGreen } });
slide10.addText('BUY on Pullbacks | Entry Zone: $200-$215', {
  x: 0.5, y: 1.25, w: 9, h: 0.6, fontSize: 20, fontFace: 'Avenir Next', bold: true, color: intuit.white, align: 'center', valign: 'middle'
});

slide10.addText('Position Sizing:', {
  x: 0.5, y: 2.0, w: 4.2, h: 0.4, fontSize: 14, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});
slide10.addText('• Growth investors: 3-5% of portfolio\n• Conservative: 1-2% of portfolio\n• Consider pairing with NVDA', {
  x: 0.5, y: 2.4, w: 4.2, h: 1.0, fontSize: 12, fontFace: 'Avenir Next', color: intuit.gray700
});

slide10.addText('Stop Loss Levels:', {
  x: 5, y: 2.0, w: 4.5, h: 0.4, fontSize: 14, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});
slide10.addText('• Conservative: $190 (below DCF)\n• Aggressive: $175 (50% Fib)\n• Monitor MI400 launch closely', {
  x: 5, y: 2.4, w: 4.5, h: 1.0, fontSize: 12, fontFace: 'Avenir Next', color: intuit.gray700
});

slide10.addText('Key Catalysts to Watch', {
  x: 0.5, y: 3.5, w: 9, h: 0.4, fontSize: 14, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

const datesData = [
  ['Q1 2026', 'H1 2026', 'Q3 2026', '2026'],
  ['Q4 Earnings', 'MI400/450 Launch', 'Oracle Supercluster', 'OpenAI Deployment']
];

slide10.addTable(datesData, {
  x: 0.5, y: 3.9, w: 9, h: 0.7,
  fontFace: 'Avenir Next',
  fontSize: 11,
  color: intuit.gray700,
  border: { pt: 0.5, color: intuit.iceBlue },
  colW: [2.25, 2.25, 2.25, 2.25],
  rowH: 0.35
});

// ============================================================
// SLIDE 11: Conclusion
// ============================================================
let slide11 = pptx.addSlide();
slide11.addShape('rect', { x: 0, y: 0, w: '100%', h: '100%', fill: { color: intuit.midnight } });
slide11.addShape('rect', { x: 0, y: 4.5, w: '100%', h: 0.8, fill: { color: intuit.superBlue } });

slide11.addText('The Verdict', {
  x: 0.5, y: 1.0, w: 9, h: 0.6, fontSize: 32, fontFace: 'Avenir Next', bold: true, color: intuit.superBlue
});

slide11.addText('AMD represents a compelling bet on the AI accelerator market\'s need for competition.', {
  x: 0.5, y: 1.8, w: 9, h: 0.8, fontSize: 18, fontFace: 'Avenir Next', color: intuit.white
});

slide11.addText('The OpenAI partnership legitimizes AMD as a top-tier supplier.\n\nAMD doesn\'t need to beat Nvidia. It just needs to show up with working products.\n\nThe supply/demand imbalance is AMD\'s greatest tailwind.', {
  x: 0.5, y: 2.7, w: 9, h: 1.5, fontSize: 14, fontFace: 'Avenir Next', color: intuit.lightBlue
});

slide11.addText('The High-Conviction #2 Play in AI Infrastructure', {
  x: 0.5, y: 4.6, w: 9, h: 0.6, fontSize: 22, fontFace: 'Avenir Next', bold: true, color: intuit.white, align: 'center'
});

// Save the presentation
const outputPath = '/Users/snandwani2/personal/research/amd-pov-2026/AMD-Investment-POV-Jan2026.pptx';
pptx.writeFile({ fileName: outputPath })
  .then(() => console.log(`✅ Presentation saved to:\n${outputPath}`))
  .catch(err => console.error('Error creating presentation:', err));


