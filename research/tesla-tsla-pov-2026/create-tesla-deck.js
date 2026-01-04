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
  teslaRed: 'E31937',
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
pptx.title = 'Tesla (TSLA) Investment POV';

// ============================================================
// SLIDE 1: Title Slide
// ============================================================
let slide1 = pptx.addSlide();
slide1.addShape('rect', { x: 0, y: 0, w: '100%', h: '100%', fill: { color: intuit.superBlue } });
slide1.addShape('rect', { x: 0, y: 4.8, w: '100%', h: 0.7, fill: { color: intuit.midnight } });

slide1.addText('Tesla Inc. (TSLA)', {
  x: 0.5, y: 1.8, w: 9, h: 1,
  fontSize: 44, fontFace: 'Avenir Next', bold: true, color: intuit.white
});
slide1.addText('Investment Point of View', {
  x: 0.5, y: 2.7, w: 9, h: 0.6,
  fontSize: 28, fontFace: 'Avenir Next', color: intuit.iceBlue
});
slide1.addText('At the Crossroads: EV Leader or AI Visionary?', {
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
  { text: 'HOLD with Caution', options: { bold: true, color: intuit.amber } }
], { x: 0.5, y: 1.3, w: 9, h: 0.4, fontSize: 18, fontFace: 'Avenir Next' });

slide2.addText([
  { text: '12-Month Price Target: ', options: { bold: true } },
  { text: '$350-$400 (Current: $438)', options: { color: intuit.gray700 } }
], { x: 0.5, y: 1.7, w: 9, h: 0.4, fontSize: 16, fontFace: 'Avenir Next', color: intuit.midnight });

const summaryBullets = [
  'Tesla lost the world\'s largest EV maker title to BYD in 2025 (1.64M vs 2.26M units)',
  'Stock trades at 230x P/E, 10x the S&P 500 average, priced for perfection',
  'Net income declined 52% YoY despite the premium valuation',
  '2026 is pivotal: FSD robotaxi, Optimus robots, lower-cost vehicles must deliver',
  'Bull case: $600+ (AI thesis plays out) | Bear case: $200-300 (valuation compression)'
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
  ['Stock Price', '$438.07', 'Down 30% from Dec highs'],
  ['Market Cap', '$1.41 Trillion', '6th largest company globally'],
  ['P/E Ratio', '230.56x', 'S&P 500 avg: ~20x'],
  ['Revenue (TTM)', '$97.69B', '+0.9% YoY'],
  ['Net Income (TTM)', '$7.13B', '-52% YoY'],
  ['2025 Deliveries', '1.64M units', '-8.6% YoY (lowest since 2022)']
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
// SLIDE 4: The Bull Thesis
// ============================================================
let slide4 = pptx.addSlide();
slide4.addShape('rect', { ...layout.iBeam, fill: { color: intuit.forestGreen } });
slide4.addText('The Bull Thesis: "More Than a Car Company"', {
  ...layout.title, fontSize: 26, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

slide4.addText('FSD & Robotaxi', {
  x: 0.5, y: 1.3, w: 4.2, h: 0.4, fontSize: 16, fontFace: 'Avenir Next', bold: true, color: intuit.forestGreen
});
slide4.addText('Robotaxi service expanding in 2026. Over 2B miles of FSD data. Potential $2-3T market by 2030.', {
  x: 0.5, y: 1.7, w: 4.2, h: 0.9, fontSize: 12, fontFace: 'Avenir Next', color: intuit.gray700
});

slide4.addText('Optimus Robot', {
  x: 5, y: 1.3, w: 4.5, h: 0.4, fontSize: 16, fontFace: 'Avenir Next', bold: true, color: intuit.forestGreen
});
slide4.addText('Humanoid robot pre-orders expected 2026. Dan Ives: "Game changer." Industrial + consumer potential.', {
  x: 5, y: 1.7, w: 4.5, h: 0.9, fontSize: 12, fontFace: 'Avenir Next', color: intuit.gray700
});

slide4.addText('Energy Storage', {
  x: 0.5, y: 2.7, w: 4.2, h: 0.4, fontSize: 16, fontFace: 'Avenir Next', bold: true, color: intuit.forestGreen
});
slide4.addText('Revenue >$10B in 2024, growing 50%+ annually. Megapack deployments accelerating globally.', {
  x: 0.5, y: 3.1, w: 4.2, h: 0.9, fontSize: 12, fontFace: 'Avenir Next', color: intuit.gray700
});

slide4.addText('Lower-Cost Vehicles', {
  x: 5, y: 2.7, w: 4.5, h: 0.4, fontSize: 16, fontFace: 'Avenir Next', bold: true, color: intuit.forestGreen
});
slide4.addText('New affordable lineup launching H1 2026. Target: 600K deliveries/quarter vs current 400K.', {
  x: 5, y: 3.1, w: 4.5, h: 0.9, fontSize: 12, fontFace: 'Avenir Next', color: intuit.gray700
});

slide4.addText('"Tesla, when it comes to physical AI plays, there\'s the godfather of AI Nvidia, and then there\'s Tesla." — Dan Ives, Wedbush', {
  x: 0.5, y: 4.2, w: 9, h: 0.6, fontSize: 12, fontFace: 'Avenir Next', italic: true, color: intuit.superBlue
});

// ============================================================
// SLIDE 5: The Bear Thesis
// ============================================================
let slide5 = pptx.addSlide();
slide5.addShape('rect', { ...layout.iBeam, fill: { color: intuit.teslaRed } });
slide5.addText('The Bear Thesis: Premium Valuation, Eroding Fundamentals', {
  ...layout.title, fontSize: 24, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

const bearPoints = [
  { text: 'Valuation Extreme: ', detail: '230x P/E is 10x S&P 500 average. Even at 75x would be 2x NVDA/MSFT/AAPL.' },
  { text: '2025 Setbacks: ', detail: 'Lost #1 EV position to BYD. Sales down 8.6%. Profits collapsed 52%.' },
  { text: 'Competition Intensifies: ', detail: 'BYD sold 2.26M EVs vs Tesla\'s 1.64M. Chinese EV makers expanding globally.' },
  { text: 'FSD Delays: ', detail: 'Timeline promised since 2016 keeps slipping. Skeptics question full autonomy claims.' },
  { text: 'Brand/Political Risk: ', detail: 'Musk\'s DOGE involvement polarizing. Consumer backlash evident in sales decline.' }
];

bearPoints.forEach((point, i) => {
  slide5.addText([
    { text: point.text, options: { bold: true, color: intuit.teslaRed } },
    { text: point.detail, options: { color: intuit.gray700 } }
  ], { x: 0.5, y: 1.3 + (i * 0.6), w: 9, h: 0.5, fontSize: 13, fontFace: 'Avenir Next' });
});

slide5.addText('"Tesla\'s forward P/E of 214 is roughly 10 times the average stock in the S&P 500... Michael Burry said Tesla stock is ridiculously overvalued." — Parkev Tatevosian, CFA', {
  x: 0.5, y: 4.3, w: 9, h: 0.6, fontSize: 11, fontFace: 'Avenir Next', italic: true, color: intuit.gray500
});

// ============================================================
// SLIDE 6: Technical Analysis
// ============================================================
let slide6 = pptx.addSlide();
slide6.addShape('rect', { ...layout.iBeam, fill: { color: intuit.superBlue } });
slide6.addText('Technical Analysis', {
  ...layout.title, fontSize: 28, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

const technicalData = [
  ['Indicator', 'Value', 'Signal'],
  ['Price', '$438.07', 'Down 2.6% (1-day)'],
  ['RSI (14)', '46.90', 'Neutral'],
  ['MACD', 'Bearish crossover', 'Caution'],
  ['vs SMA 50', 'Below ($445)', 'Short-term weakness'],
  ['vs SMA 200', 'Above ($360)', 'Long-term uptrend intact'],
  ['1-Year Return', '+74.18%', 'Strong momentum']
];

slide6.addTable(technicalData, {
  x: 0.5, y: 1.3, w: 5.5, h: 2.8,
  fontFace: 'Avenir Next',
  fontSize: 12,
  color: intuit.gray700,
  border: { pt: 0.5, color: intuit.iceBlue },
  fill: { color: intuit.white },
  colW: [1.8, 1.8, 1.9],
  rowH: 0.38
});

slide6.addText('Key Levels', {
  x: 6.2, y: 1.3, w: 3.3, h: 0.4, fontSize: 16, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

slide6.addText([
  { text: 'Support:\n', options: { bold: true, color: intuit.forestGreen } },
  { text: '• $391 (recent low)\n• $360 (200 SMA)\n• $300 (psychological)\n\n', options: { color: intuit.gray700 } },
  { text: 'Resistance:\n', options: { bold: true, color: intuit.teslaRed } },
  { text: '• $452 (R1)\n• $468 (recent high)\n• $499 (52-week high)', options: { color: intuit.gray700 } }
], { x: 6.2, y: 1.7, w: 3.3, h: 2.5, fontSize: 12, fontFace: 'Avenir Next' });

slide6.addText('Overall Signal: HOLD — Price consolidating below SMA 50, neutral RSI, long-term trend intact', {
  x: 0.5, y: 4.3, w: 9, h: 0.4, fontSize: 13, fontFace: 'Avenir Next', bold: true, color: intuit.superBlue
});

// ============================================================
// SLIDE 7: Scenario Analysis
// ============================================================
let slide7 = pptx.addSlide();
slide7.addShape('rect', { ...layout.iBeam, fill: { color: intuit.superBlue } });
slide7.addText('Scenario Analysis: 2026 Price Targets', {
  ...layout.title, fontSize: 28, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

// Bull box
slide7.addShape('rect', { x: 0.5, y: 1.3, w: 2.9, h: 2.8, fill: { color: 'E8F5E9' }, line: { color: intuit.forestGreen, pt: 2 } });
slide7.addText('BULL CASE', { x: 0.5, y: 1.35, w: 2.9, h: 0.4, fontSize: 14, fontFace: 'Avenir Next', bold: true, color: intuit.forestGreen, align: 'center' });
slide7.addText('$600-$700', { x: 0.5, y: 1.75, w: 2.9, h: 0.5, fontSize: 24, fontFace: 'Avenir Next', bold: true, color: intuit.forestGreen, align: 'center' });
slide7.addText('35% probability\n\n• Robotaxi shows traction\n• Optimus pre-orders\n• 500K+ deliveries/qtr\n• P/E sustained 150-175x', {
  x: 0.6, y: 2.3, w: 2.7, h: 1.7, fontSize: 10, fontFace: 'Avenir Next', color: intuit.gray700
});

// Base box
slide7.addShape('rect', { x: 3.55, y: 1.3, w: 2.9, h: 2.8, fill: { color: intuit.paleBlue }, line: { color: intuit.superBlue, pt: 2 } });
slide7.addText('BASE CASE', { x: 3.55, y: 1.35, w: 2.9, h: 0.4, fontSize: 14, fontFace: 'Avenir Next', bold: true, color: intuit.superBlue, align: 'center' });
slide7.addText('$350-$450', { x: 3.55, y: 1.75, w: 2.9, h: 0.5, fontSize: 24, fontFace: 'Avenir Next', bold: true, color: intuit.superBlue, align: 'center' });
slide7.addText('45% probability\n\n• Modest FSD progress\n• Flat deliveries ~400K/qtr\n• Margins compressed\n• P/E contracts to 100-125x', {
  x: 3.65, y: 2.3, w: 2.7, h: 1.7, fontSize: 10, fontFace: 'Avenir Next', color: intuit.gray700
});

// Bear box
slide7.addShape('rect', { x: 6.6, y: 1.3, w: 2.9, h: 2.8, fill: { color: 'FFEBEE' }, line: { color: intuit.teslaRed, pt: 2 } });
slide7.addText('BEAR CASE', { x: 6.6, y: 1.35, w: 2.9, h: 0.4, fontSize: 14, fontFace: 'Avenir Next', bold: true, color: intuit.teslaRed, align: 'center' });
slide7.addText('$200-$300', { x: 6.6, y: 1.75, w: 2.9, h: 0.5, fontSize: 24, fontFace: 'Avenir Next', bold: true, color: intuit.teslaRed, align: 'center' });
slide7.addText('20% probability\n\n• FSD delays continue\n• EV tax credits end\n• Competition erodes share\n• P/E compresses to 50-75x', {
  x: 6.7, y: 2.3, w: 2.7, h: 1.7, fontSize: 10, fontFace: 'Avenir Next', color: intuit.gray700
});

slide7.addText('Current price $438 reflects optimistic but not extreme assumptions. Downside risk exceeds upside in near term.', {
  x: 0.5, y: 4.3, w: 9, h: 0.4, fontSize: 12, fontFace: 'Avenir Next', italic: true, color: intuit.gray500
});

// ============================================================
// SLIDE 8: Expert Consensus
// ============================================================
let slide8 = pptx.addSlide();
slide8.addShape('rect', { ...layout.iBeam, fill: { color: intuit.superBlue } });
slide8.addText('Expert & Analyst Consensus', {
  ...layout.title, fontSize: 28, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

const expertData = [
  ['Analyst', 'Price Target', 'Key Thesis'],
  ['Dan Ives (Wedbush)', '$600+', 'AI robotics, China strength, Optimus'],
  ['Parkev Tatevosian (CFA)', '$350-$400', 'Valuation compression, EV headwinds'],
  ['Joseph (60K+ shares)', '$500-$1000+', 'FSD revenue in balance sheet'],
  ['Jo Bhakdi', '$450-$600', '"Golden year of growth" in 2026'],
  ['ARK Invest (Cathie Wood)', '$2,600 (5yr)', 'Robotaxi market dominance'],
  ['Michael Burry', 'SELL', '"Ridiculously overvalued"']
];

slide8.addTable(expertData, {
  x: 0.5, y: 1.3, w: 9, h: 2.5,
  fontFace: 'Avenir Next',
  fontSize: 12,
  color: intuit.gray700,
  border: { pt: 0.5, color: intuit.iceBlue },
  fill: { color: intuit.white },
  colW: [2.8, 2, 4.2],
  rowH: 0.36
});

slide8.addText('Consensus: Extreme divergence reflects high uncertainty. All agree 2026 is the pivotal year for Tesla\'s AI thesis.', {
  x: 0.5, y: 4.0, w: 9, h: 0.5, fontSize: 13, fontFace: 'Avenir Next', bold: true, color: intuit.superBlue
});

// ============================================================
// SLIDE 9: Investment Recommendation
// ============================================================
let slide9 = pptx.addSlide();
slide9.addShape('rect', { ...layout.iBeam, fill: { color: intuit.amber } });
slide9.addText('Investment Recommendation', {
  ...layout.title, fontSize: 28, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

slide9.addShape('rect', { x: 0.5, y: 1.25, w: 9, h: 0.6, fill: { color: intuit.amber } });
slide9.addText('HOLD with Caution | Wait for Better Entry', {
  x: 0.5, y: 1.25, w: 9, h: 0.6, fontSize: 20, fontFace: 'Avenir Next', bold: true, color: intuit.white, align: 'center', valign: 'middle'
});

slide9.addText('For Current Holders:', {
  x: 0.5, y: 2.0, w: 4.2, h: 0.4, fontSize: 14, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});
slide9.addText('• Consider trimming if >10% of portfolio\n• Hold core for AI optionality\n• Set stop-loss at $350 (200 SMA)', {
  x: 0.5, y: 2.4, w: 4.2, h: 1.0, fontSize: 12, fontFace: 'Avenir Next', color: intuit.gray700
});

slide9.addText('For New Investors:', {
  x: 5, y: 2.0, w: 4.5, h: 0.4, fontSize: 14, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});
slide9.addText('• Wait for pullback to $350-$380\n• Start small (1-2% portfolio)\n• DCA if thesis strengthens', {
  x: 5, y: 2.4, w: 4.5, h: 1.0, fontSize: 12, fontFace: 'Avenir Next', color: intuit.gray700
});

slide9.addText('Key Dates to Watch', {
  x: 0.5, y: 3.5, w: 9, h: 0.4, fontSize: 14, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

const datesData = [
  ['Q1 2026', 'H1 2026', '2026', '2026'],
  ['Delivery numbers', 'Lower-cost vehicle launch', 'Robotaxi expansion', 'Optimus pre-orders']
];

slide9.addTable(datesData, {
  x: 0.5, y: 3.9, w: 9, h: 0.7,
  fontFace: 'Avenir Next',
  fontSize: 11,
  color: intuit.gray700,
  border: { pt: 0.5, color: intuit.iceBlue },
  colW: [2.25, 2.25, 2.25, 2.25],
  rowH: 0.35
});

// ============================================================
// SLIDE 10: Conclusion
// ============================================================
let slide10 = pptx.addSlide();
slide10.addShape('rect', { x: 0, y: 0, w: '100%', h: '100%', fill: { color: intuit.midnight } });
slide10.addShape('rect', { x: 0, y: 4.5, w: '100%', h: 0.8, fill: { color: intuit.superBlue } });

slide10.addText('The Verdict', {
  x: 0.5, y: 1.0, w: 9, h: 0.6, fontSize: 32, fontFace: 'Avenir Next', bold: true, color: intuit.superBlue
});

slide10.addText('2026 will reveal whether Tesla is the next trillion-dollar AI platform or a premium automaker priced like a technology monopoly.', {
  x: 0.5, y: 1.8, w: 9, h: 0.8, fontSize: 18, fontFace: 'Avenir Next', color: intuit.white
});

slide10.addText('Tesla is the ultimate story stock. The current $1.4 trillion valuation prices in a future where robotaxis and humanoid robots generate hundreds of billions in revenue.\n\nThat future may come, but not before 2027-2028 at the earliest.\n\nMeanwhile, the core EV business faces real headwinds.', {
  x: 0.5, y: 2.7, w: 9, h: 1.5, fontSize: 14, fontFace: 'Avenir Next', color: intuit.lightBlue
});

slide10.addText('Position Accordingly.', {
  x: 0.5, y: 4.6, w: 9, h: 0.6, fontSize: 24, fontFace: 'Avenir Next', bold: true, color: intuit.white, align: 'center'
});

// Save the presentation
const outputPath = '/Users/snandwani2/personal/research/tesla-tsla-pov-2026/Tesla-TSLA-Investment-POV-Jan2026.pptx';
pptx.writeFile({ fileName: outputPath })
  .then(() => console.log(`✅ Presentation saved to:\n${outputPath}`))
  .catch(err => console.error('Error creating presentation:', err));



