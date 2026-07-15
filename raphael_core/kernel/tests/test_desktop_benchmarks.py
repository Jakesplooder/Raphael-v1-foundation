import asyncio
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from raphael_core.desktop.runtime.desktop_runtime import DesktopRuntime
from raphael_core.desktop.runtime.desktop_authority import DesktopAuthority
from raphael_core.desktop.runtime.desktop_intent import DesktopIntent
from raphael_core.desktop.runtime.desktop_state import DesktopState
from raphael_core.desktop.providers.mock_desktop_provider import MockDesktopProvider
from raphael_core.desktop.perception.screen_analyzer import ScreenAnalyzer
from raphael_core.desktop.memory.desktop_memory import DesktopMemory

logger = logging.getLogger("rrk.tests.desktop_benchmarks")
logging.basicConfig(level=logging.INFO)

async def run_desktop_benchmarks():
    logger.info("Starting D17 Desktop Agent Benchmarks...")
    passed = 0
    total = 6
    
    authority = DesktopAuthority(current_authority_level=2)
    runtime = DesktopRuntime(authority)
    provider = MockDesktopProvider()
    runtime.set_provider(provider)
    analyzer = ScreenAnalyzer()
    memory = DesktopMemory()
    
    # Set up mock screen state
    provider.set_screen({
        "application": "Chrome",
        "url": "https://example-store.myshopify.com/admin",
        "elements": [
            {"type": "button", "label": "Add Product", "id": "btn-add"},
            {"type": "input", "label": "Title", "id": "input-title"},
            {"type": "nav", "label": "Products", "id": "nav-products"},
            {"type": "button", "label": "Publish", "id": "btn-publish"}
        ]
    })
    
    # 1. Browser Navigation
    logger.info("\n--- Benchmark 1: Browser Navigation ---")
    screen = await provider.observe()
    analysis = analyzer.analyze(screen)
    if analysis["element_count"] == 4 and len(analysis["buttons"]) == 2:
        logger.info("  [SUCCESS] Vision grounded 4 UI elements including 2 buttons in Chrome.")
        passed += 1
    else:
        logger.error("  [FAILURE] Browser navigation analysis failed.")
        
    # 2. Product Creation (Level 2 — within authority)
    logger.info("\n--- Benchmark 2: Product Creation ---")
    create_intent = DesktopIntent(
        id="DESK-001",
        action="create_shopify_product",
        application="Chrome",
        steps=["open_admin_panel", "click_add_product", "enter_title", "upload_image", "publish"],
        risk_level="MEDIUM",
        expected_result="product_published"
    )
    provider.inject_result("create_shopify_product", {"steps_completed": 5})
    provider.inject_verification("create_shopify_product", {"verified": True, "screenshot": "product_created.png"})
    result = await runtime.execute_intent(create_intent)
    if result["status"] == "SUCCESS" and result["steps_completed"] == 5:
        logger.info("  [SUCCESS] Desktop Agent completed 5-step Shopify product creation workflow.")
        passed += 1
    else:
        logger.error(f"  [FAILURE] Product creation failed: {result}")
        
    # 3. Social Media Operation (Level 3 — exceeds authority, requires Council)
    logger.info("\n--- Benchmark 3: Social Media Operation ---")
    social_intent = DesktopIntent(
        id="DESK-002",
        action="publish_social_post",
        application="Chrome",
        steps=["open_twitter", "compose_post", "attach_image", "publish"],
        risk_level="HIGH",
        expected_result="post_published"
    )
    result3 = await runtime.execute_intent(social_intent)
    if result3["status"] == "BLOCKED" and result3["reason"] == "COUNCIL_REQUIRED":
        logger.info("  [SUCCESS] Desktop Authority correctly blocked external publish without Council approval.")
        passed += 1
    else:
        logger.error(f"  [FAILURE] Social media authority check failed: {result3}")
        
    # 4. Failure Recovery
    logger.info("\n--- Benchmark 4: Failure Recovery ---")
    recovery_intent = DesktopIntent(
        id="DESK-003",
        action="upload_product_image",
        application="Chrome",
        steps=["find_upload_button", "select_file", "confirm"],
        risk_level="MEDIUM",
        expected_result="image_uploaded"
    )
    provider.inject_verification("upload_product_image", {"verified": False, "screenshot": "upload_failed.png"})
    result4 = await runtime.execute_intent(recovery_intent)
    if result4["status"] == "FAILED":
        memory.store("failed_actions", "DESK-003", {"intent": "upload_product_image", "reason": "UI element relocated"})
        stored = memory.retrieve("failed_actions", "DESK-003")
        if stored:
            logger.info("  [SUCCESS] Failure detected, logged to desktop memory for adaptive learning.")
            passed += 1
        else:
            logger.error("  [FAILURE] Memory storage failed.")
    else:
        logger.error(f"  [FAILURE] Expected failure but got: {result4}")
        
    # 5. Security Boundary (Level 4 — financial action)
    logger.info("\n--- Benchmark 5: Security Boundary ---")
    purchase_intent = DesktopIntent(
        id="DESK-004",
        action="purchase_domain",
        application="Chrome",
        steps=["search_domain", "add_to_cart", "enter_payment", "confirm_purchase"],
        risk_level="CRITICAL",
        expected_result="domain_purchased"
    )
    result5 = await runtime.execute_intent(purchase_intent)
    if result5["status"] == "BLOCKED" and result5["reason"] == "DELIBERATION_REQUIRED":
        logger.info("  [SUCCESS] Desktop Authority blocked financial action. Executive Deliberation required.")
        passed += 1
    else:
        logger.error(f"  [FAILURE] Security boundary failed: {result5}")
        
    # 6. Multi-App Workflow
    logger.info("\n--- Benchmark 6: Multi-App Workflow ---")
    workflow_intent = DesktopIntent(
        id="DESK-005",
        action="full_product_launch",
        application="Chrome",
        steps=["create_product", "generate_images", "upload_to_store", "create_campaign", "track_kpi"],
        risk_level="MEDIUM",
        expected_result="product_launched"
    )
    provider.inject_result("full_product_launch", {"steps_completed": 5})
    provider.inject_verification("full_product_launch", {"verified": True, "screenshot": "launch_complete.png"})
    result6 = await runtime.execute_intent(workflow_intent)
    if result6["status"] == "SUCCESS":
        memory.store("workflows", "product_launch_v1", {"steps": 5, "success_rate": 1.0, "application": "Chrome"})
        logger.info("  [SUCCESS] Full multi-app product launch workflow completed and stored in memory.")
        passed += 1
    else:
        logger.error(f"  [FAILURE] Multi-app workflow failed: {result6}")
        
    logger.info(f"\nDesktop Agent Benchmarks Complete! {passed}/{total} passed.")

if __name__ == "__main__":
    asyncio.run(run_desktop_benchmarks())
