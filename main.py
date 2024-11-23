import re
from playwright.sync_api import Playwright, sync_playwright, expect
from six import raise_from
from playwright.async_api import async_playwright
import asyncio

hotels = []
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.booking.com/index.en-gb.html?label=gen173nr-1BCAEoggI46AdIM1gEaLUBiAEBmAEJuAEXyAEM2AEB6AEBiAIBqAIDuAKDqs25BsACAdICJGNhMDdkNTU5LTkwMTMtNGY3MS1hMTAxLWFmNmEwYTgzMTAyONgCBeACAQ&sid=d8abac8261e5e67d7f378be94403a5d0&keep_landing=1&sb_price_type=total&")
    page.wait_for_timeout(3000)

    try:
        signin_message = page.get_by_label("Dismiss sign in information.")
        signin_message.click()
    except:
        pass
    page.wait_for_timeout(1000)
    page.get_by_test_id("header-language-picker-trigger").click()
    page.wait_for_timeout(3000)
    select_language = page.get_by_test_id("All languages").get_by_role("button", name="English (US)")
    select_language.click()
    page.wait_for_timeout(3000)

    select_city = page.get_by_placeholder("Where are you going?")
    select_city.click()
    page.get_by_placeholder("Where are you going?").fill("NewYork")
    page.wait_for_timeout(1500)
    try:
        cityname = page.get_by_role("button", name="Central New York City New")
        city_name = cityname.click()

    except:
        page.get_by_role("button", name="New York New York, United").click()
        pass
    #
    page.get_by_label("24 November").click()
    page.get_by_label("24 December 2024", exact=True).click()
    page.wait_for_timeout(2000)
    
    page.get_by_test_id("occupancy-config").click()
    page.locator("div").filter(has_text=re.compile(r"^2$")).locator("button").nth(1).click()
    page.wait_for_timeout(1000)
    page.locator("div").filter(has_text=re.compile(r"^0$")).locator("button").nth(1).click()
    page.wait_for_timeout(1000)
    page.locator("div").filter(has_text=re.compile(r"^Children1$")).locator("button").nth(1).click()
    page.get_by_role("combobox").nth(1).select_option("2")
    page.wait_for_timeout(1000)
    page.get_by_role("combobox").nth(2).select_option("5")
    page.locator("div").filter(has_text=re.compile(r"^1$")).locator("button").nth(1).click()
    page.get_by_role("button", name="Done").click()
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(5000)
    page.press("body", "PageDown")
    
    page.get_by_placeholder("Search on map").click()
    page.get_by_role("heading", name="Empire State Building").click()
    page.wait_for_timeout(8000)
    
    page.get_by_placeholder("Search on map").click()
    page.get_by_placeholder("Search on map").fill("belgium")
    page.get_by_role("heading", name="Belgium", exact=True).click()
    
    page.wait_for_timeout(5000)
    
    only_show_avaiable_property = page.query_selector(
        "xpath=//html/body/div[12]/div[2]/div/div[1]/div/div/div[2]/fieldset/div[4]/label/span[3]/div/div/div")
    only_show_avaiable_property.click()
    page.wait_for_timeout(8000)
    
    for i in range(3):
        page.press("body", "PageDown")
    property_filter = page.query_selector_all("xpath=//html/body/div[.]/div[.]/div/div[.]/div/div/div[.]/fieldset")
    print(len(property_filter))
    for ratings in property_filter:
        try:
            filter = ratings.query_selector_all("div.e7c28a2436")
            for rating in filter:
                if rating.inner_text() == "5 stars" or rating.inner_text() == "No prepayment" or rating.inner_text() == "Free cancellation" or rating.inner_text() == "Very Good: 8+" or rating.inner_text() == "Air conditioning" or rating.inner_text() == "Breakfast Included":
                    rating.click()
                    print(rating.inner_text())
                    pass
                else:
                    pass
        except:
            pass
        pass
    
    page.wait_for_timeout(8000)
    page.query_selector("xpath=//html/body/div[12]/div[2]/div/div[2]/div/div/ul/li[1]/a/div[2]/div[1]/div[2]/div/div/span/span/button/span/span").click()
    page.wait_for_timeout(800)
    page.query_selector("xpath=//html/body/div[12]/div[2]/div/div[2]/div/div/ul/li[2]/a/div[2]/div[1]/div[2]/div/div/span/span/button/span/span").click()
    page.wait_for_timeout(800)
    for i in range(4):
        page.press("body", "PageDown")
        pass
    
    def getHotelsUrl():
        urls = page.query_selector_all("xpath=//html/body/div[12]/div[2]/div/div[2]/div/div/ul/li[.]")
        print(len(urls))
        for urls_links in urls:
            hotels_url = urls_links.query_selector('a')
            hotels.append(hotels_url.get_attribute("href"))
            print(hotels_url.get_attribute("href"))
    
    getHotelsUrl()
    page.wait_for_timeout(5000)
    context.close()
    browser.close()
with sync_playwright() as playwright:
    run(playwright)

# ======================================================================================================================
async def sub_categories(links):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(links)
        await page.wait_for_timeout(3000)
        await page.reload()
        await page.wait_for_timeout(5000)

        try:
            location = await page.wait_for_selector('span.hp_address_subtitle.js-hp_address_subtitle.jq_tooltip')
            print(await location.inner_text())
        except:
            print("nll")

        hotel_name = await page.query_selector('h2.d2fee87262.pp-header__title')
        print(await hotel_name.inner_text())

        await page.press("body", "PageDown")

        rating = await page.query_selector('div.a3b8729ab1.d86cee9b25')
        print(await rating.inner_text())

        await page.wait_for_timeout(4000)

        rating_star = await page.query_selector_all('span.fcd9eec8fb.d31eda6efc.c25361c37f')
        ratingstart = len(rating_star)
        print(f"{ratingstart} star")

        price = await page.query_selector('div.bui-price-display__value.prco-text-nowrap-helper.prco-inline-block-maker-helper')
        print(await price.inner_text())

        await page.wait_for_timeout(2000)
        await context.close()
        await browser.close()


async def getinfomation():
    for links in hotels:
        await sub_categories(links)
asyncio.run(getinfomation())

