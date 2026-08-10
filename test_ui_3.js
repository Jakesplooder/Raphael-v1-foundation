const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('http://localhost:8787/', {waitUntil: 'networkidle0'});
    
    // Just wait for 3 seconds
    await new Promise(r => setTimeout(r, 3000));
    
    // Get the HTML content to understand what's actually rendered
    const html = await page.content();
    fs.writeFileSync('dashboard_rendered.html', html);
    
    console.log("HTML saved to dashboard_rendered.html");
    
    await browser.close();
})();
