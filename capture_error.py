import asyncio
from playwright.async_api import async_playwright

async def capture_chat():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print("Navigating to dashboard...")
        await page.goto("http://127.0.0.1:8787")
        print("Waiting 10s for page to load...")
        await asyncio.sleep(10)
        
        # Save screenshot regardless of what's there
        path = "C:/Users/cyber/.gemini/antigravity/brain/9b3c595e-01c9-4094-8536-cc94e3ebe5ab/dashboard_error.png"
        await page.screenshot(path=path)
        print("Screenshot saved to", path)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_chat())
