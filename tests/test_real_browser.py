import asyncio
from playwright.async_api import async_playwright

async def run_browser_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print('Navigating to Dashboard...')
        await page.goto('http://127.0.0.1:8000')
        
        # Wait for chat input
        await page.wait_for_selector('#chat-input', state='visible')
        
        print('Typing into chat...')
        await page.fill('#chat-input', 'hello Raphael')
        await page.click('#chat-send-btn')
        
        print('Waiting for response...')
        await page.wait_for_selector('.chat-message.raphael:last-child', state='visible', timeout=5000)
        
        # Wait a moment for rendering
        await asyncio.sleep(1)
        
        # Take a screenshot
        await page.screenshot(path='C:\\Users\\cyber\\.gemini\\antigravity\\brain\\9b3c595e-01c9-4094-8536-cc94e3ebe5ab\\real_dashboard_chat.png')
        await browser.close()
        print('Screenshot captured!')

if __name__ == '__main__':
    asyncio.run(run_browser_test())
