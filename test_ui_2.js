const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('http://localhost:8787/dashboard', {waitUntil: 'networkidle0'});
    
    // Just wait for 5 seconds to ensure any async data loading is done
    await new Promise(r => setTimeout(r, 5000));
    
    // Take a screenshot of the page as it is
    await page.screenshot({path: 'dashboard_current.png', fullPage: true});
    
    // Get the HTML content to understand what's actually rendered
    const html = await page.content();
    fs.writeFileSync('dashboard_rendered.html', html);
    
    console.log("Screenshot saved to dashboard_current.png");
    console.log("HTML saved to dashboard_rendered.html");
    
    await browser.close();
})();
