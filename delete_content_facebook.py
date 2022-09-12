import asyncio
from playwright.async_api import async_playwright, Playwright


async def run(pw: Playwright):
    chromium = pw.chromium
    browser = await chromium.launch(headless=False)
    page = await browser.new_page()
    await page.goto("https://www.facebook.com/guidomodarelli")
    await page.pause()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())
