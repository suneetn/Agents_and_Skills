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
  ttdGreen: '00C389',
  forestGreen: '0A5C36',
  amber: 'F5A623',
  coral: 'FF6B6B',
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
pptx.title = 'The Trade Desk (TTD) Investment POV';

// ============================================================
// SLIDE 1: Title Slide
// ============================================================
let slide1 = pptx.addSlide();
slide1.addShape('rect', { x: 0, y: 0, w: '100%', h: '100%', fill: { color: intuit.superBlue } });
slide1.addShape('rect', { x: 0, y: 4.8, w: '100%', h: 0.7, fill: { color: intuit.midnight } });

slide1.addText('The Trade Desk (TTD)', {
  x: 0.5, y: 1.8, w: 9, h: 1,
  fontSize: 44, fontFace: 'Avenir Next', bold: true, color: intuit.white
});
slide1.addText('Investment Point of View', {
  x: 0.5, y: 2.7, w: 9, h: 0.6,
  fontSize: 28, fontFace: 'Avenir Next', color: intuit.iceBlue
});
slide1.addText('A Contrarian Opportunity or Falling Knife?', {
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
slide2.addShape('rect', { ...layout.iBeam, fill: { color: intuit.coral } });
slide2.addText('Executive Summary', {
  ...layout.title, fontSize: 28, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

slide2.addText([
  { text: 'Investment Rating: ', options: { bold: true, color: intuit.midnight } },
  { text: 'SPECULATIVE BUY', options: { bold: true, color: intuit.amber } }
], { x: 0.5, y: 1.3, w: 9, h: 0.4, fontSize: 18, fontFace: 'Avenir Next' });

slide2.addText([
  { text: '12-Month Price Target: ', options: { bold: true } },
  { text: '$50-$65 (Current: $37.68) → 33-72% Upside', options: { color: intuit.gray700 } }
], { x: 0.5, y: 1.7, w: 9, h: 0.4, fontSize: 16, fontFace: 'Avenir Next', color: intuit.midnight });

const summaryBullets = [
  'Stock down 62% YTD, trading near 52-week low at $37.68',
  'Cheapest valuation ever: 20x forward P/E (historical avg: 80-100x)',
  'Still growing 18% annually while industry grows 6-8%',
  'Key risks: Amazon DSP expansion, management shakeup, Kokai rollout',
  'Analyst consensus: $80+ price target (114% implied upside)'
];

slide2.addText(summaryBullets.map(b => ({ text: b, options: { bullet: true, paraSpaceAfter: 10 } })), {
  x: 0.5, y: 2.2, w: 9, h: 2.8, fontSize: 15, fontFace: 'Avenir Next', color: intuit.gray700, valign: 'top'
});

// ============================================================
// SLIDE 3: The Numbers
// ============================================================
let slide3 = pptx.addSlide();
slide3.addShape('rect', { ...layout.iBeam, fill: { color: intuit.superBlue } });
slide3.addText('The Numbers: A Tale of Two Stories', {
  ...layout.title, fontSize: 26, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

const metricsData = [
  ['Metric', 'Value', 'Context'],
  ['Stock Price', '$37.68', '-62% YTD (near 52-wk low)'],
  ['Market Cap', '$18.5B', 'Down from $60B peak'],
  ['P/E (TTM)', '42.8x', 'Cheapest in company history'],
  ['Forward P/E', '20x', 'Historical avg: 80-100x'],
  ['Revenue (TTM)', '$2.44B', '+26% YoY'],
  ['Net Income', '$393M', '+120% YoY'],
  ['ROIC', '25.7%', 'Up from 5% in 2022']
];

slide3.addTable(metricsData, {
  x: 0.5, y: 1.3, w: 9, h: 3.2,
  fontFace: 'Avenir Next',
  fontSize: 12,
  color: intuit.gray700,
  border: { pt: 0.5, color: intuit.iceBlue },
  fill: { color: intuit.white },
  colW: [2.2, 2.2, 4.6],
  rowH: 0.38,
  align: 'left',
  valign: 'middle'
});

slide3.addText('The business is performing. The stock is not.', {
  x: 0.5, y: 4.5, w: 9, h: 0.4, fontSize: 13, fontFace: 'Avenir Next', italic: true, color: intuit.superBlue
});

// ============================================================
// SLIDE 4: Why The Stock Crashed
// ============================================================
let slide4 = pptx.addSlide();
slide4.addShape('rect', { ...layout.iBeam, fill: { color: intuit.coral } });
slide4.addText('Why The Stock Crashed 62% in 2025', {
  ...layout.title, fontSize: 26, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

const crashReasons = [
  { text: '1. Amazon DSP Expansion: ', detail: 'Amazon partnered with Netflix, other streamers. Marketers can bypass TTD entirely.' },
  { text: '2. Management Shakeup: ', detail: 'New COO, new CFO, multiple senior departures since March. Investors hate instability.' },
  { text: '3. Kokai Platform Issues: ', detail: 'AI platform rollout caused first revenue miss in 33 quarters.' },
  { text: '4. Jefferies Downgrade: ', detail: 'Cut to Hold at $40 in Dec 2025, triggering institutional selling.' }
];

crashReasons.forEach((point, i) => {
  slide4.addText([
    { text: point.text, options: { bold: true, color: intuit.coral } },
    { text: point.detail, options: { color: intuit.gray700 } }
  ], { x: 0.5, y: 1.3 + (i * 0.7), w: 9, h: 0.65, fontSize: 13, fontFace: 'Avenir Next' });
});

slide4.addText('"Amazon\'s DSP allows marketers to skip the trade desk altogether." — CFA Analysis', {
  x: 0.5, y: 4.3, w: 9, h: 0.5, fontSize: 11, fontFace: 'Avenir Next', italic: true, color: intuit.gray500
});

// ============================================================
// SLIDE 5: The Bull Thesis
// ============================================================
let slide5 = pptx.addSlide();
slide5.addShape('rect', { ...layout.iBeam, fill: { color: intuit.ttdGreen } });
slide5.addText('Bull Thesis: Contrarian Opportunity', {
  ...layout.title, fontSize: 26, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

const bullPoints = [
  { text: 'Cheapest Ever Valuation: ', detail: '20x forward P/E vs 80-100x historical. "The cheapest this stock has been, arguably ever."' },
  { text: 'Still Gaining Market Share: ', detail: 'Growing 18% while ad industry grows 6-8%. Outpacing Google/YouTube.' },
  { text: 'ROIC Recovery: ', detail: 'Improved from 5% (2022) to 25.7% today. Business model is working.' },
  { text: 'No Conflict of Interest: ', detail: 'Only works with buy-side. Unlike Google/Meta/Amazon, no inventory to push.' },
  { text: 'CFA Price Target: ', detail: 'Parkev Tatevosian sees $60-65 by end of 2026 (50%+ upside).' }
];

bullPoints.forEach((point, i) => {
  slide5.addText([
    { text: point.text, options: { bold: true, color: intuit.ttdGreen } },
    { text: point.detail, options: { color: intuit.gray700 } }
  ], { x: 0.5, y: 1.3 + (i * 0.6), w: 9, h: 0.55, fontSize: 12, fontFace: 'Avenir Next' });
});

slide5.addText('"This is the cheapest you\'ve been able to buy this stock going back several years." — Parkev CFA', {
  x: 0.5, y: 4.3, w: 9, h: 0.5, fontSize: 11, fontFace: 'Avenir Next', italic: true, color: intuit.gray500
});

// ============================================================
// SLIDE 6: The Bear Thesis
// ============================================================
let slide6 = pptx.addSlide();
slide6.addShape('rect', { ...layout.iBeam, fill: { color: intuit.coral } });
slide6.addText('Bear Thesis: Legitimate Risks', {
  ...layout.title, fontSize: 26, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

const bearPoints = [
  { text: 'Amazon is Formidable: ', detail: 'First-party purchase data, Netflix deal, vertically integrated. Existential threat.' },
  { text: 'Walled Gardens Winning: ', detail: 'Google, Meta, Amazon control most digital ad spend. Open internet is shrinking.' },
  { text: 'Management Instability: ', detail: 'Too many C-suite changes in one year. New CFO is ex-VC, not operator.' },
  { text: 'Kokai Must Deliver: ', detail: 'If AI platform fails to gain traction, TTD loses tech edge.' },
  { text: 'Economic Sensitivity: ', detail: 'Ad budgets are first to be cut in recession.' }
];

bearPoints.forEach((point, i) => {
  slide6.addText([
    { text: point.text, options: { bold: true, color: intuit.coral } },
    { text: point.detail, options: { color: intuit.gray700 } }
  ], { x: 0.5, y: 1.3 + (i * 0.6), w: 9, h: 0.55, fontSize: 12, fontFace: 'Avenir Next' });
});

slide6.addText('"Investors are always skeptical when a management shakeup is so abrupt and so large." — CFA Analysis', {
  x: 0.5, y: 4.3, w: 9, h: 0.5, fontSize: 11, fontFace: 'Avenir Next', italic: true, color: intuit.gray500
});

// ============================================================
// SLIDE 7: Technical Analysis
// ============================================================
let slide7 = pptx.addSlide();
slide7.addShape('rect', { ...layout.iBeam, fill: { color: intuit.superBlue } });
slide7.addText('Technical Analysis: Near Rock Bottom', {
  ...layout.title, fontSize: 28, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

const technicalData = [
  ['Indicator', 'Value', 'Signal'],
  ['Price', '$37.68', 'Near 52-week low ($35.65)'],
  ['1-Year Return', '-62.49%', 'Brutal selloff'],
  ['RSI (14)', '58.68', 'Neutral (recovering)'],
  ['MACD', 'Bullish crossover', 'Early positive'],
  ['vs SMA 200', 'Below ($57.05)', 'Strong downtrend'],
  ['Fibonacci', '100% retracement', 'All gains erased']
];

slide7.addTable(technicalData, {
  x: 0.5, y: 1.3, w: 5.5, h: 2.5,
  fontFace: 'Avenir Next',
  fontSize: 11,
  color: intuit.gray700,
  border: { pt: 0.5, color: intuit.iceBlue },
  fill: { color: intuit.white },
  colW: [1.8, 1.8, 1.9],
  rowH: 0.35
});

slide7.addText('Key Levels', {
  x: 6.2, y: 1.3, w: 3.3, h: 0.4, fontSize: 16, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

slide7.addText([
  { text: 'Support:\n', options: { bold: true, color: intuit.ttdGreen } },
  { text: '• $35.65 (52-wk low)\n• $36.90 (S1)\n\n', options: { color: intuit.gray700 } },
  { text: 'Resistance:\n', options: { bold: true, color: intuit.coral } },
  { text: '• $41.92 (50 SMA)\n• $57.05 (200 SMA)\n• $127.59 (52-wk high)', options: { color: intuit.gray700 } }
], { x: 6.2, y: 1.7, w: 3.3, h: 2.3, fontSize: 11, fontFace: 'Avenir Next' });

slide7.addText('Signal: HOLD with bullish MACD crossover. Watch $35 support.', {
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
slide8.addShape('rect', { x: 0.5, y: 1.3, w: 2.9, h: 2.8, fill: { color: 'E8F5E9' }, line: { color: intuit.ttdGreen, pt: 2 } });
slide8.addText('BULL CASE', { x: 0.5, y: 1.35, w: 2.9, h: 0.4, fontSize: 14, fontFace: 'Avenir Next', bold: true, color: intuit.ttdGreen, align: 'center' });
slide8.addText('$80-$100', { x: 0.5, y: 1.75, w: 2.9, h: 0.5, fontSize: 24, fontFace: 'Avenir Next', bold: true, color: intuit.ttdGreen, align: 'center' });
slide8.addText('25% probability\n\n• Kokai gains traction\n• Amazon fears overblown\n• CTV accelerates\n• P/E re-rates to 35-40x', {
  x: 0.6, y: 2.3, w: 2.7, h: 1.7, fontSize: 10, fontFace: 'Avenir Next', color: intuit.gray700
});

// Base box
slide8.addShape('rect', { x: 3.55, y: 1.3, w: 2.9, h: 2.8, fill: { color: intuit.paleBlue }, line: { color: intuit.superBlue, pt: 2 } });
slide8.addText('BASE CASE', { x: 3.55, y: 1.35, w: 2.9, h: 0.4, fontSize: 14, fontFace: 'Avenir Next', bold: true, color: intuit.superBlue, align: 'center' });
slide8.addText('$50-$65', { x: 3.55, y: 1.75, w: 2.9, h: 0.5, fontSize: 24, fontFace: 'Avenir Next', bold: true, color: intuit.superBlue, align: 'center' });
slide8.addText('50% probability\n\n• 15-20% revenue growth\n• Management stabilizes\n• P/E stays 20-25x\n• EPS progresses to $2.50+', {
  x: 3.65, y: 2.3, w: 2.7, h: 1.7, fontSize: 10, fontFace: 'Avenir Next', color: intuit.gray700
});

// Bear box
slide8.addShape('rect', { x: 6.6, y: 1.3, w: 2.9, h: 2.8, fill: { color: 'FFEBEE' }, line: { color: intuit.coral, pt: 2 } });
slide8.addText('BEAR CASE', { x: 6.6, y: 1.35, w: 2.9, h: 0.4, fontSize: 14, fontFace: 'Avenir Next', bold: true, color: intuit.coral, align: 'center' });
slide8.addText('$25-$35', { x: 6.6, y: 1.75, w: 2.9, h: 0.5, fontSize: 24, fontFace: 'Avenir Next', bold: true, color: intuit.coral, align: 'center' });
slide8.addText('25% probability\n\n• Amazon takes share\n• Kokai fails\n• Mgmt turnover continues\n• Recession cuts budgets', {
  x: 6.7, y: 2.3, w: 2.7, h: 1.7, fontSize: 10, fontFace: 'Avenir Next', color: intuit.gray700
});

slide8.addText('Analyst consensus: $80 target = 114% upside from current price.', {
  x: 0.5, y: 4.3, w: 9, h: 0.4, fontSize: 12, fontFace: 'Avenir Next', italic: true, color: intuit.gray500
});

// ============================================================
// SLIDE 9: CFA Price Target Model
// ============================================================
let slide9 = pptx.addSlide();
slide9.addShape('rect', { ...layout.iBeam, fill: { color: intuit.ttdGreen } });
slide9.addText('CFA Price Target Analysis (2027 EPS: $2.46)', {
  ...layout.title, fontSize: 26, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

const ptData = [
  ['Forward P/E', 'Price Target', 'Upside from $39'],
  ['20x (current)', '$49', '+26%'],
  ['25x', '$62', '+59%'],
  ['30x', '$74', '+90%'],
  ['35x (historical)', '$86', '+120%']
];

slide9.addTable(ptData, {
  x: 0.5, y: 1.3, w: 5.5, h: 2.2,
  fontFace: 'Avenir Next',
  fontSize: 14,
  color: intuit.gray700,
  border: { pt: 0.5, color: intuit.iceBlue },
  fill: { color: intuit.white },
  colW: [2.0, 1.75, 1.75],
  rowH: 0.42
});

slide9.addText('Key Insight', {
  x: 6.2, y: 1.3, w: 3.3, h: 0.4, fontSize: 16, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

slide9.addText('Even at current depressed valuation (20x forward), EPS progression alone could drive stock to $49.\n\nIf sentiment improves and P/E expands to historical 35x, stock could more than double.', {
  x: 6.2, y: 1.7, w: 3.3, h: 2.0, fontSize: 12, fontFace: 'Avenir Next', color: intuit.gray700
});

slide9.addText('"I think Trade Desk stock trades for $60-$65 by end of 2026. That would be ~50% upside." — Parkev CFA', {
  x: 0.5, y: 4.0, w: 9, h: 0.5, fontSize: 13, fontFace: 'Avenir Next', italic: true, color: intuit.superBlue
});

// ============================================================
// SLIDE 10: Investment Recommendation
// ============================================================
let slide10 = pptx.addSlide();
slide10.addShape('rect', { ...layout.iBeam, fill: { color: intuit.amber } });
slide10.addText('Investment Recommendation', {
  ...layout.title, fontSize: 28, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

slide10.addShape('rect', { x: 0.5, y: 1.25, w: 9, h: 0.6, fill: { color: intuit.amber } });
slide10.addText('SPECULATIVE BUY | High Risk / High Reward', {
  x: 0.5, y: 1.25, w: 9, h: 0.6, fontSize: 20, fontFace: 'Avenir Next', bold: true, color: intuit.white, align: 'center', valign: 'middle'
});

slide10.addText('Entry Strategy:', {
  x: 0.5, y: 2.0, w: 4.2, h: 0.4, fontSize: 14, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});
slide10.addText('• Current price acceptable for risk-tolerant\n• Scale in on dips to $35 support\n• Full position if holds 52-week low', {
  x: 0.5, y: 2.4, w: 4.2, h: 1.0, fontSize: 12, fontFace: 'Avenir Next', color: intuit.gray700
});

slide10.addText('Position Sizing:', {
  x: 5, y: 2.0, w: 4.5, h: 0.4, fontSize: 14, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});
slide10.addText('• Conservative: 1-2% max\n• Growth-oriented: 2-3%\n• NOT a core holding at this stage', {
  x: 5, y: 2.4, w: 4.5, h: 1.0, fontSize: 12, fontFace: 'Avenir Next', color: intuit.gray700
});

slide10.addText('Key Catalysts to Watch', {
  x: 0.5, y: 3.5, w: 9, h: 0.4, fontSize: 14, fontFace: 'Avenir Next', bold: true, color: intuit.midnight
});

const datesData = [
  ['Feb 2026', 'Q1 2026', 'Throughout 2026', 'H2 2026'],
  ['Q4 Earnings', 'CTV Upfronts', 'Management Updates', 'Economic Data']
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

slide11.addText('The Trade Desk is either a broken growth story being correctly de-rated, OR a quality company at a generational valuation.', {
  x: 0.5, y: 1.8, w: 9, h: 0.8, fontSize: 17, fontFace: 'Avenir Next', color: intuit.white
});

slide11.addText('The business fundamentals (18% growth, 81% margins, 25.7% ROIC) are solid.\n\nBut competitive and execution risks are real.\n\nAt 20x forward P/E, the risk/reward is asymmetric to the upside.', {
  x: 0.5, y: 2.7, w: 9, h: 1.5, fontSize: 14, fontFace: 'Avenir Next', color: intuit.lightBlue
});

slide11.addText('Speculative Buy for Contrarians Willing to Bet Against the Crowd', {
  x: 0.5, y: 4.6, w: 9, h: 0.6, fontSize: 20, fontFace: 'Avenir Next', bold: true, color: intuit.white, align: 'center'
});

// Save the presentation
const outputPath = '/Users/snandwani2/personal/research/trade-desk-pov-2026/Trade-Desk-TTD-Investment-POV-Jan2026.pptx';
pptx.writeFile({ fileName: outputPath })
  .then(() => console.log(`✅ Presentation saved to:\n${outputPath}`))
  .catch(err => console.error('Error creating presentation:', err));


