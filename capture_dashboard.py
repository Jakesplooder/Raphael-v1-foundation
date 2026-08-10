import asyncio
from playwright.async_api import async_playwright

async def capture_chat():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print("Navigating to dashboard...")
        await page.goto("http://127.0.0.1:8787")
        print("Waiting for chat interface to load...")
        
        await page.wait_for_selector("textarea#chat-input", timeout=120000)
        
        # Type the command
        await page.fill("textarea#chat-input", "generate an image of a cyberpunk city")
        await page.keyboard.press("Enter") # Wait, is it Enter or click button? The button is <button onclick="sendChat()">.
        # It's a textarea, Enter might just add a newline. So I will click the button.
        await page.click("button.primary:has-text('Send to Raphael')")
        
        print("Waiting for response...")
        # Wait until the response is rendered. The response has the class 'chat-content'.
        # Since I can't know when it appears easily except by text, I will just sleep.
        await asyncio.sleep(8)
        
        # Save screenshot
        path = "C:/Users/cyber/.gemini/antigravity/brain/9b3c595e-01c9-4094-8536-cc94e3ebe5ab/dashboard_chat_ui_render.png"
        await page.screenshot(path=path)
        print("Screenshot saved to", path)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_chat())
