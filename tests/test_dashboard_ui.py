import asyncio
import httpx
from playwright.async_api import async_playwright

async def run_ui_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Load the dashboard
        await page.goto("http://localhost:8000")
        
        # Wait for the WebSocket to connect
        await page.wait_for_selector("#ws-status-pill", state="attached")
        print("Dashboard loaded.")
        
        print("\n--- Triggering Test Lifecycle via API ---")
        async def trigger():
            async with httpx.AsyncClient() as client:
                resp = await client.post("http://127.0.0.1:8788/api/test-trigger", timeout=10.0)
                resp.raise_for_status()
                
        asyncio.create_task(trigger())
            
        print("Waiting for job_started...")
        await page.wait_for_selector(".job-card[data-job-id='test_job_1']", timeout=5000)
        status = await page.locator(".job-card[data-job-id='test_job_1']").get_attribute("data-status")
        print(f"Card 1 status: {status}")
        
        print("Waiting for running...")
        await page.wait_for_selector(".job-card[data-job-id='test_job_1'][data-status='running']", timeout=5000)
        status = await page.locator(".job-card[data-job-id='test_job_1']").get_attribute("data-status")
        text = await page.locator(".job-card[data-job-id='test_job_1'] .job-status").inner_text()
        print(f"Card 1 status: {status} | Text: {text}")
        
        print("Waiting for retrying...")
        await page.wait_for_selector(".job-card[data-job-id='test_job_1'][data-status='retrying']", timeout=5000)
        status = await page.locator(".job-card[data-job-id='test_job_1']").get_attribute("data-status")
        text = await page.locator(".job-card[data-job-id='test_job_1'] .job-status").inner_text()
        print(f"Card 1 status: {status} | Text: {text}")
        
        print("Waiting for failed...")
        await page.wait_for_selector(".job-card[data-job-id='test_job_1'][data-status='failed']", timeout=5000)
        status = await page.locator(".job-card[data-job-id='test_job_1']").get_attribute("data-status")
        text = await page.locator(".job-card[data-job-id='test_job_1'] .job-status").inner_text()
        print(f"Card 1 status: {status} | Text: {text}")
        
        print("Waiting for job 2 (asset generated)...")
        await page.wait_for_selector(".job-card[data-job-id='test_job_2'][data-status='completed']", timeout=5000)
        
        status = await page.locator(".job-card[data-job-id='test_job_2']").get_attribute("data-status")
        img_src = await page.locator(".job-card[data-job-id='test_job_2'] .job-thumb").get_attribute("src")
        
        # Verify it rendered a real image, not a broken placeholder
        img_handle = await page.locator(".job-card[data-job-id='test_job_2'] .job-thumb").element_handle()
        is_real_image = await page.evaluate("""async (el) => {
            if (el.complete && el.naturalWidth > 0) return true;
            if (el.complete && el.naturalWidth === 0) return false;
            return new Promise((resolve) => {
                el.onload = () => resolve(el.naturalWidth > 0);
                el.onerror = () => resolve(false);
            });
        }""", img_handle)
        print(f"Card 2 status: {status} | Thumbnail src: {img_src} | Real Image Rendered: {is_real_image}")
        
        print("\n--- Testing Connection Status Banner ---")
        await page.evaluate("""
            const event = new MessageEvent('message', {
                data: JSON.stringify({ type: "BRIDGE_DISCONNECTED" })
            });
            wsConnection.onmessage(event);
        """)
        
        await page.wait_for_selector("#connection-status-banner", state="visible", timeout=2000)
        banner_text = await page.locator("#connection-status-banner").inner_text()
        print(f"Banner status after disconnect: {banner_text}")
        
        await page.evaluate("""
            const event = new MessageEvent('message', {
                data: JSON.stringify({ type: "BRIDGE_RECONNECTED" })
            });
            wsConnection.onmessage(event);
        """)
        
        await page.wait_for_selector("#connection-status-banner", state="hidden", timeout=2000)
        print("Banner status after reconnect: hidden")
        
        await page.screenshot(path="C:\\Users\\cyber\\.gemini\\antigravity\\brain\\9b3c595e-01c9-4094-8536-cc94e3ebe5ab\\ui_test_result.png")
        await browser.close()
        print("Done!")

if __name__ == "__main__":
    asyncio.run(run_ui_test())
