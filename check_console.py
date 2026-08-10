import asyncio
from playwright.async_api import async_playwright

async def capture_chat():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.on("console", lambda msg: print(f"Browser console: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"Browser error: {exc}"))
        print("Navigating to dashboard...")
        await page.goto("http://127.0.0.1:8787")
        await asyncio.sleep(10)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_chat())
