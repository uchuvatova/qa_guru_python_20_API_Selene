import json
import logging
import random

import requests
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from requests import Response
from selene import browser
from selene.support.conditions import have
import allure
from conftest import browser_management

WEB_URL = "https://demowebshop.tricentis.com"
API_URL = "https://demowebshop.tricentis.com"


def demoshop_api_post(url, **kwargs):
    with step("API Request"):
        result = requests.post(url=API_URL + url, **kwargs)
        allure.attach(body=result.request.url, name="Request url",
                      attachment_type=AttachmentType.TEXT)
        allure.attach(body=result.request.method, name="Request method",
                      attachment_type=AttachmentType.TEXT)
        allure.attach(body=json.dumps(result.request.body, indent=4, ensure_ascii=True), name="Request body",
                      attachment_type=AttachmentType.JSON, extension="json")
        allure.attach(body=json.dumps(result.json(), indent=4, ensure_ascii=True), name="Response body",
                      attachment_type=AttachmentType.JSON, extension="json")
        allure.attach(body=str(result.cookies), name="Response cookies", attachment_type=AttachmentType.TEXT,
                      extension="txt")

        logging.info(result.request.url)
        logging.info(result.request.method)
        logging.info(result.request.body)
        logging.info(result.status_code)
        logging.info(result.text)
        logging.info(result.cookies)
    return result


def test_add_one_item_though_api(browser_management):
    url = "/addproducttocart/catalog/45/1/1"

    with step("Добавить товар из каталога через API"):
        result: Response = demoshop_api_post(url)
    with step("Получить cookie из API"):
        cookie = result.cookies.get("Nop.customer")
    with step("Передать cookie в браузер"):
        browser.open(WEB_URL)
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
    with step("Открыть страницу Корзины покупок"):
        browser.element('#topcartlink').click()

    browser.element(".qty-input").should(have.value("1"))


def test_add_some_items_though_api(browser_management):
    count_items = random.randint(1, 10)
    url = f"/addproducttocart/catalog/45/1/{count_items}"

    with step("Добавить несколько единиц товара из каталога через API"):
        result: Response = demoshop_api_post(url)

    with step("Получить cookie из API"):
        cookie = result.cookies.get("Nop.customer")
    with step("Передать cookie в браузер"):
        browser.open(WEB_URL)
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
    with step("Открыть страницу Корзины покупок"):
        browser.element('#topcartlink').click()

    browser.element(".qty-input").should(have.value(f"{count_items}"))
