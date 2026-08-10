const puppeteer = require("puppeteer");

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    await page.setViewport({ width: 1280, height: 1024 });

    console.log("Navigating to http://localhost:8787/");
    await page.goto("http://localhost:8787/", {waitUntil: "domcontentloaded"});
    console.log("Navigated");
    
    await new Promise(r => setTimeout(r, 2000));
    
    try {
        console.log("JS-clicking button[data-page=\"chat\"]");
        await page.evaluate(() => {
            const btn = document.querySelector("button[data-page=\"chat\"]");
            if(btn) btn.click();
        });
        
        console.log("Clicked! Waiting 1s...");
        await new Promise(r => setTimeout(r, 1000));
        
        console.log("Checking if #chat-input exists");
        const exists = await page.evaluate(() => !!document.querySelector("#chat-input"));
        console.log("#chat-input exists?", exists);
        
        if (exists) {
            console.log("Typing into #chat-input");
            await page.type("#chat-input", "refresh command center");
            console.log("JS-clicking send button");
            await page.evaluate(() => {
                const btn = document.querySelector("button[onclick=\"sendChat()\"]");
                if(btn) btn.click();
            });
            console.log("Chat sent! Waiting 10s for the system to process the command...");
            await new Promise(r => setTimeout(r, 10000));
            
            console.log("Going back to Home page");
            await page.evaluate(() => {
                const btn = document.querySelector("button[data-page=\"home\"]");
                if(btn) btn.click();
            });
            await new Promise(r => setTimeout(r, 1000));
        }
    } catch(err) {
        console.error("Test failed:", err);
    }
    
    await page.screenshot({path: "ui_test_result_final.png", fullPage: true});

    const activeJobsText = await page.evaluate(() => {
        const panel = document.getElementById("active-jobs-panel");
        return panel ? panel.outerHTML : "Active Jobs panel not found";
    });
    console.log("Active Jobs panel HTML:");
    console.log(activeJobsText);
    
    await browser.close();
})();
