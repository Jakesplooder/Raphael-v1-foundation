const puppeteer = require("puppeteer");

(async () => {
    const browser = await puppeteer.launch({dumpio: true});
    const page = await browser.newPage();
    page.on("console", msg => console.log("PAGE LOG:", msg.text()));
    page.on("pageerror", err => console.log("PAGE ERROR:", err.toString()));
    
    console.log("Navigating to http://localhost:8787/");
    await page.goto("http://localhost:8787/", {waitUntil: "domcontentloaded"});
    console.log("Navigated");
    
    await new Promise(r => setTimeout(r, 2000));
    
    try {
        console.log("Clicking button[data-page=\"chat\"]");
        await page.click("button[data-page=\"chat\"]");
        console.log("Clicked! Waiting 1s...");
        await new Promise(r => setTimeout(r, 1000));
        
        console.log("Checking if #chat-input exists");
        const exists = await page.evaluate(() => !!document.querySelector("#chat-input"));
        console.log("#chat-input exists?", exists);
        
        if (!exists) {
            console.log("DOM body:", await page.evaluate(() => document.body.innerHTML));
        } else {
            console.log("Typing into #chat-input");
            await page.type("#chat-input", "generate an image of a cyberpunk city");
            console.log("Clicking send");
            await page.click("button[onclick=\"sendChat()\"]");
            console.log("Chat sent! Waiting 6s...");
            await new Promise(r => setTimeout(r, 6000));
        }
        
    } catch(err) {
        console.error("Test failed:", err);
    }
    await browser.close();
})();
