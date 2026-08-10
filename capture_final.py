import asyncio
from playwright.async_api import async_playwright

async def capture_chat():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print("Navigating to dashboard...")
        await page.goto("http://127.0.0.1:8787")
        print("Waiting 15s for page to load...")
        await asyncio.sleep(15)
        
        print("Injecting JS to fill chat and click...")
        await page.evaluate('''() => {
            const input = document.getElementById("chat-input");
            if (input) {
                input.value = "generate an image of a cyberpunk city";
                const btn = Array.from(document.querySelectorAll('button')).find(el => el.textContent.includes('Send to Raphael'));
                if (btn) btn.click();
            }
        }''')
        
        print("Waiting 5s for response...")
        await asyncio.sleep(5)
        
        # Save screenshot
        path = "C:/Users/cyber/.gemini/antigravity/brain/9b3c595e-01c9-4094-8536-cc94e3ebe5ab/dashboard_chat_final.png"
        await page.screenshot(path=path)
        print("Screenshot saved to", path)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_chat())
