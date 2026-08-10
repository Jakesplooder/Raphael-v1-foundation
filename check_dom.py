import asyncio
from playwright.async_api import async_playwright

async def capture_chat():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:8787")
        await asyncio.sleep(10)
        content = await page.content()
        if "chat-input" in content:
            print("chat-input FOUND in DOM")
        else:
            print("chat-input NOT FOUND in DOM")
            if "Dashboard Chat" in content:
                print("But Dashboard Chat text IS found")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_chat())
