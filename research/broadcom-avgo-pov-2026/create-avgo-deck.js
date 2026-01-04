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
  coral: 'FF6B6B',
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
pptx.title = 'Broadcom (AVGO) Investment POV';

// ============================================================
// SLIDE 1: Title Slide
// ============================================================
let slide = pptx.addSlide();
slide.background = { color: intuit.superBlue };

slide.addText('Broadcom Inc. (AVGO)', {
  x: 0.5, y: 2.0, w: 9.0, h: 1.0,
  fontSize: 54, fontFace: 'Avenir Next', bold: true,
  color: intuit.white, align: 'center'
});

slide.addText('Investment Point of View', {
  x: 0.5, y: 3.1, w: 9.0, h: 0.5,
  fontSize: 28, fontFace: 'Avenir Next',
  color: intuit.lightBlue, align: 'center'
});

slide.addText('January 2026', {
  x: 0.5, y: 4.8, w: 9.0, h: 0.4,
  fontSize: 18, fontFace: 'Avenir Next',
  color: intuit.iceBlue, align: 'center'
});

// ============================================================
// SLIDE 2: Executive Summary
// ============================================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };
slide.addShape('rect', { ...layout.iBeam, fill: { color: intuit.superBlue } });

slide.addText('Executive Summary', {
  ...layout.title,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight, valign: 'top'
});

slide.addText([
  { text: 'Investment Rating: ', options: { bold: true, color: intuit.midnight } },
  { text: 'HOLD', options: { bold: true, color: intuit.amber } },
  { text: ' at current levels, ', options: { color: intuit.gray700 } },
  { text: 'BUY', options: { bold: true, color: intuit.forestGreen } },
  { text: ' on dips to $320-330', options: { color: intuit.gray700 } },
  { text: '\n\n', options: {} },
  { text: 'Key Thesis:\n', options: { bold: true, color: intuit.midnight } },
  { text: 'Broadcom owns the custom silicon and networking fabric that powers AI inference at scale. While NVIDIA dominates training GPUs, Broadcom captures the inference market where hyperscalers need custom chips optimized for their specific workloads.', options: { color: intuit.gray700 } },
  { text: '\n\n', options: {} },
  { text: 'Catalysts:\n', options: { bold: true, color: intuit.midnight } },
  { text: '• OpenAI partnership: $10B+ order for custom AI chips\n', options: { color: intuit.gray700 } },
  { text: '• AI backlog: $73B through FY2027 (vs. $38B consensus)\n', options: { color: intuit.gray700 } },
  { text: '• 5 hyperscaler customers: Google, Meta, ByteDance, OpenAI, and potentially Microsoft', options: { color: intuit.gray700 } }
], {
  ...layout.content,
  fontSize: 18, fontFace: 'Avenir Next',
  valign: 'top', paraSpaceAfter: 6
});

// ============================================================
// SLIDE 3: Section - Financial Performance
// ============================================================
slide = pptx.addSlide();
slide.background = { color: intuit.midnight };
slide.addShape('rect', { ...layout.iBeam, fill: { color: intuit.superBlue } });

slide.addText('Financial Performance', {
  x: 0.5, y: 2.3, w: 8.0, h: 1.0,
  fontSize: 44, fontFace: 'Avenir Next', bold: true,
  color: intuit.white
});

slide.addText('FY2025 Results & Key Metrics', {
  x: 0.5, y: 3.4, w: 8.0, h: 0.5,
  fontSize: 22, fontFace: 'Avenir Next',
  color: intuit.lightBlue
});

// ============================================================
// SLIDE 4: Key Metrics
// ============================================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };
slide.addShape('rect', { ...layout.iBeam, fill: { color: intuit.superBlue } });

slide.addText('Key Financial Metrics', {
  ...layout.title,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight, valign: 'top'
});

// Metrics row
const metrics = [
  { value: '$63.9B', label: 'Revenue', change: '+24% YoY' },
  { value: '$23.1B', label: 'Net Income', change: '+292% YoY' },
  { value: '$27B', label: 'Free Cash Flow', change: 'Strong' },
  { value: '72.7x', label: 'P/E Ratio', change: 'Premium' }
];

metrics.forEach((m, i) => {
  const xPos = 0.5 + (i * 2.4);
  slide.addText(m.value, {
    x: xPos, y: 1.6, w: 2.2, h: 0.8,
    fontSize: 36, fontFace: 'Avenir Next', bold: true,
    color: intuit.superBlue, align: 'center'
  });
  slide.addText(m.label, {
    x: xPos, y: 2.4, w: 2.2, h: 0.4,
    fontSize: 16, fontFace: 'Avenir Next',
    color: intuit.midnight, align: 'center'
  });
  slide.addText(m.change, {
    x: xPos, y: 2.8, w: 2.2, h: 0.3,
    fontSize: 14, fontFace: 'Avenir Next',
    color: m.change.includes('+') ? intuit.forestGreen : intuit.gray500, align: 'center'
  });
});

// Stock info box
slide.addShape('rect', {
  x: 0.5, y: 3.4, w: 9.0, h: 1.6,
  fill: { color: intuit.paleBlue }
});

slide.addText([
  { text: 'Current Price: ', options: { bold: true } },
  { text: '$347.62', options: { color: intuit.superBlue, bold: true } },
  { text: '   |   52-Week Range: ', options: { bold: true } },
  { text: '$138.10 - $414.61', options: {} },
  { text: '   |   YoY Return: ', options: { bold: true } },
  { text: '+116%', options: { color: intuit.forestGreen, bold: true } }
], {
  x: 0.7, y: 3.6, w: 8.6, h: 0.5,
  fontSize: 16, fontFace: 'Avenir Next',
  color: intuit.midnight, align: 'center'
});

slide.addText([
  { text: 'Market Cap: ', options: { bold: true } },
  { text: '$1.64 Trillion', options: {} },
  { text: '   |   Gross Margin: ', options: { bold: true } },
  { text: '68%', options: {} },
  { text: '   |   EBITDA Margin: ', options: { bold: true } },
  { text: '35%', options: {} }
], {
  x: 0.7, y: 4.2, w: 8.6, h: 0.5,
  fontSize: 16, fontFace: 'Avenir Next',
  color: intuit.midnight, align: 'center'
});

// ============================================================
// SLIDE 5: AI Strategy
// ============================================================
slide = pptx.addSlide();
slide.background = { color: intuit.midnight };
slide.addShape('rect', { ...layout.iBeam, fill: { color: intuit.superBlue } });

slide.addText('AI Strategy Deep Dive', {
  x: 0.5, y: 2.3, w: 8.0, h: 1.0,
  fontSize: 44, fontFace: 'Avenir Next', bold: true,
  color: intuit.white
});

slide.addText('Custom Accelerators & Networking', {
  x: 0.5, y: 3.4, w: 8.0, h: 0.5,
  fontSize: 22, fontFace: 'Avenir Next',
  color: intuit.lightBlue
});

// ============================================================
// SLIDE 6: Custom AI Thesis
// ============================================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };
slide.addShape('rect', { ...layout.iBeam, fill: { color: intuit.superBlue } });

slide.addText('The Custom Accelerator Thesis', {
  ...layout.title,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight, valign: 'top'
});

slide.addText([
  { text: 'Why Custom Chips Beat General-Purpose GPUs for Inference:\n\n', options: { bold: true, color: intuit.superBlue } },
  { text: '1. ', options: { bold: true } },
  { text: 'Training vs. Inference: ', options: { bold: true, color: intuit.midnight } },
  { text: 'Training happens episodically; inference runs continuously at massive scale\n\n', options: { color: intuit.gray700 } },
  { text: '2. ', options: { bold: true } },
  { text: 'Efficiency Gains: ', options: { bold: true, color: intuit.midnight } },
  { text: 'Custom chips deliver 3-5x better performance per watt vs. general GPUs\n\n', options: { color: intuit.gray700 } },
  { text: '3. ', options: { bold: true } },
  { text: 'Cost Savings: ', options: { bold: true, color: intuit.midnight } },
  { text: 'At ChatGPT scale, efficiency improvements save tens of billions annually\n\n', options: { color: intuit.gray700 } },
  { text: '4. ', options: { bold: true } },
  { text: 'Workload Optimization: ', options: { bold: true, color: intuit.midnight } },
  { text: 'Chips designed for specific model architectures outperform generic solutions', options: { color: intuit.gray700 } }
], {
  x: 0.5, y: 1.4, w: 9.0, h: 4.0,
  fontSize: 18, fontFace: 'Avenir Next',
  valign: 'top'
});

// ============================================================
// SLIDE 7: Customer Base
// ============================================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };
slide.addShape('rect', { ...layout.iBeam, fill: { color: intuit.superBlue } });

slide.addText('Elite Hyperscaler Customer Base', {
  ...layout.title,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight, valign: 'top'
});

// Customer table
const customers = [
  ['Google', 'TPU (Tensor Processing Unit)', 'Long-standing, 3M+ units/year'],
  ['Meta', 'Custom AI Accelerator', 'Active partner'],
  ['ByteDance', 'Custom AI Accelerator', 'Active partner'],
  ['OpenAI', 'Custom Inference Chip', 'NEW: $10B+ order'],
  ['Microsoft', 'Unknown', 'Potential 5th customer']
];

// Table header
slide.addShape('rect', {
  x: 0.5, y: 1.5, w: 9.0, h: 0.5,
  fill: { color: intuit.superBlue }
});

slide.addText(['Customer', 'Product', 'Status'].join('                    '), {
  x: 0.5, y: 1.5, w: 9.0, h: 0.5,
  fontSize: 14, fontFace: 'Avenir Next', bold: true,
  color: intuit.white, valign: 'middle'
});

customers.forEach((row, i) => {
  const yPos = 2.1 + (i * 0.55);
  const bgColor = i % 2 === 0 ? intuit.paleBlue : intuit.white;
  const isNew = row[2].includes('NEW');
  
  slide.addShape('rect', {
    x: 0.5, y: yPos, w: 9.0, h: 0.5,
    fill: { color: bgColor }
  });
  
  slide.addText(row[0], {
    x: 0.6, y: yPos, w: 2.0, h: 0.5,
    fontSize: 14, fontFace: 'Avenir Next', bold: true,
    color: intuit.midnight, valign: 'middle'
  });
  
  slide.addText(row[1], {
    x: 2.8, y: yPos, w: 3.5, h: 0.5,
    fontSize: 14, fontFace: 'Avenir Next',
    color: intuit.gray700, valign: 'middle'
  });
  
  slide.addText(row[2], {
    x: 6.5, y: yPos, w: 2.8, h: 0.5,
    fontSize: 14, fontFace: 'Avenir Next', bold: isNew,
    color: isNew ? intuit.forestGreen : intuit.gray700, valign: 'middle'
  });
});

// AI Revenue callout
slide.addShape('rect', {
  x: 0.5, y: 4.9, w: 9.0, h: 0.6,
  fill: { color: intuit.iceBlue }
});

slide.addText([
  { text: 'AI Semiconductor Revenue: ', options: { bold: true } },
  { text: '~$12B (+220% YoY)', options: { color: intuit.forestGreen, bold: true } },
  { text: '   |   ', options: {} },
  { text: 'AI Backlog: ', options: { bold: true } },
  { text: '$73B through FY2027', options: { color: intuit.superBlue, bold: true } }
], {
  x: 0.5, y: 4.9, w: 9.0, h: 0.6,
  fontSize: 16, fontFace: 'Avenir Next',
  color: intuit.midnight, align: 'center', valign: 'middle'
});

// ============================================================
// SLIDE 8: OpenAI Partnership
// ============================================================
slide = pptx.addSlide();
slide.background = { color: intuit.paleBlue };

slide.addShape('rect', { ...layout.iBeam, fill: { color: intuit.superBlue } });

slide.addText('"', {
  x: 0.3, y: 1.0, w: 1.0, h: 1.0,
  fontSize: 120, fontFace: 'Georgia',
  color: intuit.superBlue
});

slide.addText('The most significant catalyst: OpenAI partnership validates the custom silicon thesis. Their $10B+ order for AI racks represents the beginning of a transformative relationship.', {
  x: 1.2, y: 1.8, w: 7.5, h: 2.0,
  fontSize: 26, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight, valign: 'top'
});

slide.addText([
  { text: 'OpenAI chose Broadcom to reduce NVIDIA dependence and optimize for ChatGPT inference workloads. ', options: { color: intuit.gray700 } },
  { text: 'Manufacturing capacity secured with TSMC; first chips expected 2026.', options: { color: intuit.gray700 } }
], {
  x: 1.2, y: 3.5, w: 7.5, h: 1.0,
  fontSize: 18, fontFace: 'Avenir Next',
  valign: 'top'
});

// ============================================================
// SLIDE 9: Technical Analysis
// ============================================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };
slide.addShape('rect', { ...layout.iBeam, fill: { color: intuit.superBlue } });

slide.addText('Technical Analysis', {
  ...layout.title,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight, valign: 'top'
});

// Technical indicators
const techMetrics = [
  { label: 'RSI (14)', value: '25.09', signal: 'Oversold', color: intuit.forestGreen },
  { label: 'MACD', value: '-5.82', signal: 'Bearish', color: intuit.coral },
  { label: 'vs 50-day SMA', value: 'Below', signal: 'Weak', color: intuit.amber },
  { label: 'vs 200-day SMA', value: 'Above', signal: 'Healthy', color: intuit.forestGreen }
];

techMetrics.forEach((m, i) => {
  const xPos = 0.5 + (i * 2.4);
  slide.addText(m.value, {
    x: xPos, y: 1.6, w: 2.2, h: 0.6,
    fontSize: 28, fontFace: 'Avenir Next', bold: true,
    color: intuit.superBlue, align: 'center'
  });
  slide.addText(m.label, {
    x: xPos, y: 2.2, w: 2.2, h: 0.3,
    fontSize: 14, fontFace: 'Avenir Next',
    color: intuit.gray700, align: 'center'
  });
  slide.addText(m.signal, {
    x: xPos, y: 2.5, w: 2.2, h: 0.3,
    fontSize: 14, fontFace: 'Avenir Next', bold: true,
    color: m.color, align: 'center'
  });
});

// Key levels
slide.addText('Key Price Levels:', {
  x: 0.5, y: 3.2, w: 9.0, h: 0.4,
  fontSize: 18, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight
});

slide.addText([
  { text: 'Support: ', options: { bold: true, color: intuit.forestGreen } },
  { text: '$340 (Fib 23.6%), $325 (local min), $305 (Fib 38.2%)\n', options: { color: intuit.gray700 } },
  { text: 'Resistance: ', options: { bold: true, color: intuit.coral } },
  { text: '$370, $386, $415 (52-week high)\n', options: { color: intuit.gray700 } },
  { text: 'Trading Signal: ', options: { bold: true, color: intuit.superBlue } },
  { text: 'HOLD — Stock is oversold (RSI 25) after recent pullback. Wait for RSI recovery above 30 or support at $325-340.', options: { color: intuit.gray700 } }
], {
  x: 0.5, y: 3.6, w: 9.0, h: 1.5,
  fontSize: 16, fontFace: 'Avenir Next',
  valign: 'top'
});

// ============================================================
// SLIDE 10: Bull vs Bear
// ============================================================
slide = pptx.addSlide();
slide.background = { color: intuit.white };
slide.addShape('rect', { ...layout.iBeam, fill: { color: intuit.superBlue } });

slide.addText('Investment Considerations', {
  ...layout.title,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.midnight, valign: 'top'
});

// Bull case
slide.addShape('rect', {
  x: 0.5, y: 1.4, w: 4.3, h: 3.5,
  fill: { color: 'E8FFE8' }
});

slide.addText('Bull Case', {
  x: 0.5, y: 1.5, w: 4.3, h: 0.5,
  fontSize: 20, fontFace: 'Avenir Next', bold: true,
  color: intuit.forestGreen, align: 'center'
});

slide.addText([
  { text: '✓ AI custom accelerator demand (+220%)\n\n' },
  { text: '✓ OpenAI validates custom silicon thesis\n\n' },
  { text: '✓ 5 hyperscaler customers\n\n' },
  { text: '✓ AI networking moat (Tomahawk)\n\n' },
  { text: '✓ VMware recurring revenue\n\n' },
  { text: '✓ Strong FCF ($27B)' }
], {
  x: 0.7, y: 2.0, w: 4.0, h: 2.8,
  fontSize: 14, fontFace: 'Avenir Next',
  color: intuit.gray700, valign: 'top'
});

// Bear case
slide.addShape('rect', {
  x: 5.2, y: 1.4, w: 4.3, h: 3.5,
  fill: { color: 'FFE8E8' }
});

slide.addText('Bear Case', {
  x: 5.2, y: 1.5, w: 4.3, h: 0.5,
  fontSize: 20, fontFace: 'Avenir Next', bold: true,
  color: intuit.coral, align: 'center'
});

slide.addText([
  { text: '⚠ Premium valuation (72x PE)\n\n' },
  { text: '⚠ Customer concentration (top 10 = 50%)\n\n' },
  { text: '⚠ Competition from customer tooling\n\n' },
  { text: '⚠ NVIDIA expanding into networking\n\n' },
  { text: '⚠ In-sourcing changes business model\n\n' },
  { text: '⚠ Non-AI segments sluggish' }
], {
  x: 5.4, y: 2.0, w: 4.0, h: 2.8,
  fontSize: 14, fontFace: 'Avenir Next',
  color: intuit.gray700, valign: 'top'
});

// ============================================================
// SLIDE 11: Recommendation
// ============================================================
slide = pptx.addSlide();
slide.background = { color: intuit.superBlue };

slide.addText('Investment Recommendation', {
  x: 0.5, y: 1.0, w: 9.0, h: 0.8,
  fontSize: 40, fontFace: 'Avenir Next', bold: true,
  color: intuit.white, align: 'center'
});

slide.addText('HOLD', {
  x: 0.5, y: 2.0, w: 9.0, h: 1.0,
  fontSize: 72, fontFace: 'Avenir Next', bold: true,
  color: intuit.white, align: 'center'
});

slide.addText('at current price ($347.62)', {
  x: 0.5, y: 3.0, w: 9.0, h: 0.5,
  fontSize: 24, fontFace: 'Avenir Next',
  color: intuit.lightBlue, align: 'center'
});

// Action boxes
slide.addShape('rect', {
  x: 0.5, y: 3.7, w: 4.3, h: 1.0,
  fill: { color: intuit.forestGreen }
});

slide.addText([
  { text: 'BUY on dips to $320-330\n', options: { bold: true, fontSize: 18 } },
  { text: 'Strong entry if RSI confirms reversal', options: { fontSize: 14 } }
], {
  x: 0.5, y: 3.7, w: 4.3, h: 1.0,
  fontFace: 'Avenir Next',
  color: intuit.white, align: 'center', valign: 'middle'
});

slide.addShape('rect', {
  x: 5.2, y: 3.7, w: 4.3, h: 1.0,
  fill: { color: intuit.navy }
});

slide.addText([
  { text: 'Price Targets\n', options: { bold: true, fontSize: 18 } },
  { text: 'Conservative: $380 | Bull: $535 (HSBC)', options: { fontSize: 14 } }
], {
  x: 5.2, y: 3.7, w: 4.3, h: 1.0,
  fontFace: 'Avenir Next',
  color: intuit.white, align: 'center', valign: 'middle'
});

// ============================================================
// SLIDE 12: Key Takeaways
// ============================================================
slide = pptx.addSlide();
slide.background = { color: intuit.midnight };
slide.addShape('rect', { ...layout.iBeam, fill: { color: intuit.superBlue } });

slide.addText('Key Takeaways', {
  x: 0.5, y: 0.5, w: 9.0, h: 0.7,
  fontSize: 36, fontFace: 'Avenir Next', bold: true,
  color: intuit.white
});

slide.addText([
  { text: '1. ', options: { bold: true, color: intuit.superBlue } },
  { text: 'Broadcom ≠ NVIDIA', options: { bold: true, color: intuit.white } },
  { text: ' — Complementary, not competitive. NVIDIA owns training; Broadcom owns inference + networking.\n\n', options: { color: intuit.lightBlue } },
  
  { text: '2. ', options: { bold: true, color: intuit.superBlue } },
  { text: 'OpenAI partnership is transformative', options: { bold: true, color: intuit.white } },
  { text: ' — Validates custom silicon thesis, opens door to other frontier model developers.\n\n', options: { color: intuit.lightBlue } },
  
  { text: '3. ', options: { bold: true, color: intuit.superBlue } },
  { text: 'AI backlog provides visibility', options: { bold: true, color: intuit.white } },
  { text: ' — $73B through FY2027, with potential for upside surprises.\n\n', options: { color: intuit.lightBlue } },
  
  { text: '4. ', options: { bold: true, color: intuit.superBlue } },
  { text: 'Technically oversold', options: { bold: true, color: intuit.white } },
  { text: ' — RSI at 25 suggests near-term bounce; wait for confirmation.\n\n', options: { color: intuit.lightBlue } },
  
  { text: '5. ', options: { bold: true, color: intuit.superBlue } },
  { text: 'Premium valuation justified', options: { bold: true, color: intuit.white } },
  { text: ' — AI leadership position and growth rate support premium multiple.', options: { color: intuit.lightBlue } }
], {
  x: 0.5, y: 1.4, w: 9.0, h: 4.0,
  fontSize: 17, fontFace: 'Avenir Next',
  valign: 'top'
});

// ============================================================
// SLIDE 13: Thank You
// ============================================================
slide = pptx.addSlide();
slide.background = { color: intuit.superBlue };

slide.addText('Thank You', {
  x: 0.5, y: 2.2, w: 9.0, h: 1.0,
  fontSize: 54, fontFace: 'Avenir Next', bold: true,
  color: intuit.white, align: 'center'
});

slide.addText('Questions & Discussion', {
  x: 0.5, y: 3.3, w: 9.0, h: 0.5,
  fontSize: 24, fontFace: 'Avenir Next',
  color: intuit.lightBlue, align: 'center'
});

slide.addText('Research Date: January 3, 2026', {
  x: 0.5, y: 4.8, w: 9.0, h: 0.4,
  fontSize: 14, fontFace: 'Avenir Next',
  color: intuit.iceBlue, align: 'center'
});

// Save the presentation
const outputPath = '/Users/snandwani2/personal/research/broadcom-avgo-pov-2026/Broadcom-AVGO-Investment-POV-Jan2026.pptx';
pptx.writeFile({ fileName: outputPath })
  .then(() => {
    console.log(`✅ Presentation created successfully!`);
    console.log(`📍 Location: ${outputPath}`);
  })
  .catch(err => {
    console.error('Error creating presentation:', err);
  });


