"""
Screenshot script for LeetCode interactive demos.
Uses Playwright (headless Chromium) to capture screenshots of each demo page.
"""
import os
import sys
import asyncio
from pathlib import Path

async def take_screenshots():
    from playwright.async_api import async_playwright

    base_dir = Path(__file__).parent.parent
    demos = [
        {
            "name": "furthest-building",
            "path": base_dir / "furthest-building" / "index.html",
            "output_dir": base_dir / "furthest-building" / "output",
        },
        {
            "name": "range-sum-query",
            "path": base_dir / "range-sum-query" / "index.html",
            "output_dir": base_dir / "range-sum-query" / "output",
        },
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        for demo in demos:
            print(f"\n📸 Capturing screenshots for: {demo['name']}")

            # Create output directory
            demo["output_dir"].mkdir(parents=True, exist_ok=True)

            file_url = demo["path"].resolve().as_uri()

            # Desktop viewport
            page = await browser.new_page(viewport={"width": 1400, "height": 900})
            await page.goto(file_url)
            await page.wait_for_timeout(2000)  # Wait for fonts & animations

            # Full page screenshot
            await page.screenshot(
                path=str(demo["output_dir"] / "desktop_full.png"),
                full_page=True
            )
            print(f"  ✅ Desktop full-page screenshot saved")

            # Viewport screenshot
            await page.screenshot(
                path=str(demo["output_dir"] / "desktop_viewport.png"),
                full_page=False
            )
            print(f"  ✅ Desktop viewport screenshot saved")

            # Interact with the page for demo-specific screenshots
            if demo["name"] == "furthest-building":
                # Click step forward a few times
                for i in range(4):
                    btn = page.locator("#btn-step")
                    if await btn.is_enabled():
                        await btn.click()
                        await page.wait_for_timeout(500)

                await page.screenshot(
                    path=str(demo["output_dir"] / "desktop_mid_simulation.png"),
                    full_page=True
                )
                print(f"  ✅ Mid-simulation screenshot saved")

                # Auto-play to completion
                auto_btn = page.locator("#btn-auto")
                await auto_btn.click()
                await page.wait_for_timeout(5000)

                await page.screenshot(
                    path=str(demo["output_dir"] / "desktop_completed.png"),
                    full_page=True
                )
                print(f"  ✅ Completed simulation screenshot saved")

            elif demo["name"] == "range-sum-query":
                # Do a query
                await page.fill("#query-left", "1")
                await page.fill("#query-right", "4")
                await page.click("button:has-text('Query Sum')")
                await page.wait_for_timeout(1000)

                await page.screenshot(
                    path=str(demo["output_dir"] / "desktop_after_query.png"),
                    full_page=True
                )
                print(f"  ✅ After-query screenshot saved")

                # Do an update
                await page.fill("#update-idx", "2")
                await page.fill("#update-val", "15")
                await page.click("button:has-text('Update')")
                await page.wait_for_timeout(1000)

                await page.screenshot(
                    path=str(demo["output_dir"] / "desktop_after_update.png"),
                    full_page=True
                )
                print(f"  ✅ After-update screenshot saved")

            await page.close()

            # Tablet viewport
            page = await browser.new_page(viewport={"width": 768, "height": 1024})
            await page.goto(file_url)
            await page.wait_for_timeout(1500)
            await page.screenshot(
                path=str(demo["output_dir"] / "tablet_viewport.png"),
                full_page=False
            )
            print(f"  ✅ Tablet viewport screenshot saved")
            await page.close()

        await browser.close()
        print("\n✨ All screenshots captured successfully!")

if __name__ == "__main__":
    asyncio.run(take_screenshots())
