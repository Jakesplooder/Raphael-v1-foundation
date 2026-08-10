import asyncio
from playwright.async_api import async_playwright

async def run_browser_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print('Navigating to Dashboard...')
        await page.goto('http://127.0.0.1:8787')
        
        # Wait for the app to be loaded (overview API takes 12 seconds)
        print('Waiting for overview API to finish and UI to render...')
        
        # Click the chat tab
        await page.wait_for_selector('button[data-page="chat"]', state='visible', timeout=30000)
        await page.click('button[data-page="chat"]')
            
        await page.wait_for_selector('#chat-input', state='visible', timeout=10000)
        print('Typing into chat...')
        await page.fill('#chat-input', 'generate an image of a cyberpunk city')
        
        # Send using Ctrl+Enter
        await page.press('#chat-input', 'Control+Enter')
        
        print('Waiting for response...')
        await page.wait_for_selector('.chat-message.raphael:last-child', state='visible', timeout=15000)
        
        await asyncio.sleep(1)
        
        text = await page.locator('.chat-message.raphael:last-child').inner_text()
        print('UI RESPONSE:', text)
        
        await page.screenshot(path='C:\\Users\\cyber\\.gemini\\antigravity\\brain\\9b3c595e-01c9-4094-8536-cc94e3ebe5ab\\real_dashboard_chat_generate.png')
        await browser.close()
        print('Screenshot captured!')

if __name__ == '__main__':
    asyncio.run(run_browser_test())
