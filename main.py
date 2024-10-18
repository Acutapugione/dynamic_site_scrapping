import asyncio
from playwright.async_api import async_playwright, Playwright, Browser, TimeoutError


BASE_URL = "https://goiteens.com/"

PYTHON_PROJECTS = BASE_URL + "project-packages-categories/python/"


async def extract(page) -> set[str]:
    st = set()
    await page.goto(PYTHON_PROJECTS)
    projects = page.locator(".projects-category-list")
    await projects.wait_for()
    # print(len(await projects.first.locator("a").all()))

    for link in await projects.first.locator("a.project-card").all():
        url = await link.get_attribute("href")
        st.add(url)
        # print(f"{url=}")
    return st


async def extract_youtube_lnk(browser: Browser, link: str) -> str | None:
    try:
        page = await browser.new_page()
        await page.goto(link)
        item = page.locator(
            "section.single-project__content > div > figure > div > iframe"
        )  # body > div.goiteens__content > main > section.single-project__content > div > figure > div > iframe
        await item.wait_for()
        data = await item.get_attribute("data-src")
        if data:
            return data
        youtube_iframe = page.locator("figure > iframe")
        await youtube_iframe.wait_for()
        data = await youtube_iframe.get_attribute("data-src")
        return data
        # st.add(data)
    except TimeoutError as e:
        print(f"{e=}")


async def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = await chromium.launch(headless=False)
    page = await browser.new_page()
    # EXTRACT
    extracted = await extract(page)
    youtube_links = await asyncio.gather(
        *(extract_youtube_lnk(browser=browser, link=x) for x in extracted)
    )
    # youtube_links = await extract_youtube_lnk(browser, extracted)
    print(f"{youtube_links=}")
    # figure > iframe
    await browser.close()
    # TRANSFORM

    # LOAD


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
