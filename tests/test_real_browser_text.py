import asyncio
from playwright.async_api import async_playwright

async def run_browser_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto('http://127.0.0.1:8000')
        await page.wait_for_selector('#chat-input', state='visible')
        
        await page.fill('#chat-input', 'hello Raphael')
        await page.click('#chat-send-btn')
        
        await page.wait_for_selector('.chat-message.raphael:last-child', state='visible', timeout=5000)
        
        text = await page.locator('.chat-message.raphael:last-child').inner_text()
        print('UI RESPONSE:', text)
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run_browser_test())
