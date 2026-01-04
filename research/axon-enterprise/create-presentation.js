const pptxgen = require('pptxgenjs');
const path = require('path');

// Get the html2pptx library path
const html2pptxPath = path.join(process.env.HOME, '.claude/skills/pptx/scripts/html2pptx.js');
const html2pptx = require(html2pptxPath);

async function createAxonPresentation() {
    const pptx = new pptxgen();
    
    // Set presentation properties
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = 'AI Stock Analyst';
    pptx.title = 'Axon Enterprise (AXON) - Investment Analysis';
    pptx.subject = 'Comprehensive stock analysis and investment recommendation';
    
    const slidesDir = path.join(__dirname, 'slides');
    
    console.log('Creating AXON presentation...');
    
    // Slide 1: Title
    console.log('Processing slide 1: Title');
    await html2pptx(path.join(slidesDir, 'slide1-title.html'), pptx);
    
    // Slide 2: Company Overview
    console.log('Processing slide 2: Company Overview');
    await html2pptx(path.join(slidesDir, 'slide2-overview.html'), pptx);
    
    // Slide 3: Financial Performance
    console.log('Processing slide 3: Financial Performance');
    await html2pptx(path.join(slidesDir, 'slide3-financials.html'), pptx);
    
    // Slide 4: Valuation Analysis
    console.log('Processing slide 4: Valuation Analysis');
    await html2pptx(path.join(slidesDir, 'slide4-valuation.html'), pptx);
    
    // Slide 5: Technical Analysis
    console.log('Processing slide 5: Technical Analysis');
    await html2pptx(path.join(slidesDir, 'slide5-technical.html'), pptx);
    
    // Slide 6: Growth Catalysts
    console.log('Processing slide 6: Growth Catalysts');
    await html2pptx(path.join(slidesDir, 'slide6-catalysts.html'), pptx);
    
    // Slide 7: Investment Recommendation
    console.log('Processing slide 7: Investment Recommendation');
    await html2pptx(path.join(slidesDir, 'slide7-recommendation.html'), pptx);
    
    // Slide 8: Conclusion
    console.log('Processing slide 8: Conclusion');
    await html2pptx(path.join(slidesDir, 'slide8-conclusion.html'), pptx);
    
    // Save the presentation
    const outputPath = path.join(__dirname, 'AXON-Investment-Analysis.pptx');
    await pptx.writeFile({ fileName: outputPath });
    
    console.log(`\nPresentation created successfully!`);
    console.log(`Output: ${outputPath}`);
}

createAxonPresentation().catch(err => {
    console.error('Error creating presentation:', err);
    process.exit(1);
});



