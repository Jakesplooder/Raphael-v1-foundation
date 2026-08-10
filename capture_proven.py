import asyncio
from playwright.async_api import async_playwright

async def capture_chat():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print("Navigating to dashboard...")
        await page.goto("http://127.0.0.1:8787")
        print("Waiting for chat input...")
        await page.wait_for_selector("textarea#chat-input", timeout=60000)
        
        print("Filling chat input...")
        await page.fill("textarea#chat-input", "generate an image of a cyberpunk city")
        
        print("Clicking send button...")
        await page.click("button.primary:has-text('Send to Raphael')")
        
        print("Waiting for response text to appear...")
        # Wait for the response text to appear in the DOM
        await page.wait_for_function("document.body.innerText.includes('No matching workflow found')")
        
        print("Response received, waiting 2s for animations...")
        await asyncio.sleep(2)
        
        # Save screenshot
        path = "C:/Users/cyber/.gemini/antigravity/brain/9b3c595e-01c9-4094-8536-cc94e3ebe5ab/dashboard_chat_proven.png"
        await page.screenshot(path=path)
        print("Screenshot saved to", path)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_chat())
