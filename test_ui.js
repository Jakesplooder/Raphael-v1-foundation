const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('http://localhost:8787/', {waitUntil: 'networkidle0'});
    
    // Wait for the UI to be interactive
    await new Promise(r => setTimeout(r, 2000));
    
    // Try to click the "chat" button or trigger the chat view
    // The button has ID 'view-toggle' or similar? Let's just click 'Classic View' or similar if needed.
    // Or just type into the input if it's there
    try {
        await page.click('button[data-page="chat"]');
        await new Promise(r => setTimeout(r, 1000));
        
        await page.waitForSelector('#chat-input', {timeout: 5000});
        await page.type('#chat-input', 'generate an image of a cyberpunk city');
        
        // Find the send button
        await page.click('button[onclick="sendChat()"]');
        
        console.log("Chat sent. Waiting for UI update...");
        await new Promise(r => setTimeout(r, 6000));
        
    } catch(err) {
        console.log("Could not find #chat-input or send button. Taking screenshot anyway.");
    }

    // Take a screenshot of the updated page
    await page.screenshot({path: 'dashboard_with_plan.png', fullPage: true});
    
    // Output the text of the Active Jobs section to see what's there
    const activeJobsText = await page.evaluate(() => {
        const h2s = Array.from(document.querySelectorAll('h2'));
        const activeJobsH2 = h2s.find(h2 => h2.textContent && h2.textContent.includes('Active Jobs'));
        if (activeJobsH2 && activeJobsH2.parentElement) {
            return activeJobsH2.parentElement.textContent;
        }
        return 'Active Jobs section not found';
    });
    console.log("Active Jobs section text:");
    console.log(activeJobsText);
    
    await browser.close();
})();
