import asyncio
from playwright.async_api import async_playwright

async def capture_chat():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Set a large viewport
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        print("Navigating to dashboard...")
        await page.goto("http://127.0.0.1:8787")
        print("Waiting 10s...")
        await asyncio.sleep(10)
        
        print("Filling chat input via evaluate...")
        await page.evaluate('''() => {
            const input = document.getElementById("chat-input");
            if (input) {
                input.value = "generate an image of a cyberpunk city";
            } else {
                console.error("No chat input found");
            }
        }''')
        
        print("Clicking via evaluate...")
        await page.evaluate('''() => {
            if (typeof sendChat === 'function') {
                sendChat();
            } else {
                const btn = Array.from(document.querySelectorAll('button')).find(el => el.textContent.includes('Send to Raphael'));
                if (btn) btn.click();
            }
        }''')
        
        print("Waiting 10s for response to render...")
        await asyncio.sleep(10)
        
        # Save screenshot
        path = "C:/Users/cyber/.gemini/antigravity/brain/9b3c595e-01c9-4094-8536-cc94e3ebe5ab/dashboard_chat_proven.png"
        await page.screenshot(path=path, full_page=True)
        print("Screenshot saved to", path)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_chat())
