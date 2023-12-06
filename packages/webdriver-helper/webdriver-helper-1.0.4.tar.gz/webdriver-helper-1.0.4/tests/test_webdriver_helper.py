import shutil
from pathlib import Path

import pytest
from selenium.webdriver.common.by import By
from webdriver_helper import (
    get_chrome_manager,
    get_geckodriver_manager,
    get_webdriver,
    session,
)
from webdriver_manager.core.driver_cache import DriverCache


@pytest.fixture(
    params=[
        "chrome",
        "firefox",
        "ie",
    ]
)
def driver_type(request):
    if request.param == "ie":
        session.proxies = {
            "http": "socks5://127.0.0.1:1080",
            "https": "socks5://127.0.0.1:1080",
        }
    else:
        session.proxies = {}

    return request.param


@pytest.fixture(scope="session", autouse=True)
def remove_case():
    case = DriverCache()
    path = Path(case._root_dir)
    if path.exists():
        shutil.rmtree(case._root_dir)


@pytest.fixture(scope="session")
def chrome_manager():
    return get_chrome_manager()


@pytest.fixture(scope="session")
def firefox_manager():
    return get_geckodriver_manager()


def test_chrome_driver_url(chrome_manager):
    url = chrome_manager.driver.get_url()
    assert "https://registry.npmmirror.com/" in url


def test_chrome_driver_version(chrome_manager):
    url = chrome_manager.driver.get_latest_release_version()
    # assert url.startswith("9")
    assert "." in url


def test_firefox_driver_url(firefox_manager):
    url = firefox_manager.driver.get_url()
    assert "https://registry.npmmirror.com/" in url


def test_get_webdriver(driver_type):

    with get_webdriver(driver_type) as driver:
        driver.get("https://baidu.com")
        html = driver.page_source

        assert "百度" in html


@pytest.mark.skip("todo")
@pytest.mark.parametrize(
    "args, kwargs",
    [
        ((), {}),
        ((), {"a": 2}),
        (({"a": 1}), {}),
        (({"a": 1}), {"a": 2}),
    ],
)
def test_debugger(args, kwargs):
    assert 0


def test_upload_by_drop(driver_type):

    with get_webdriver(driver_type) as driver:
        driver.get("http://118.24.147.95:8086/upload.html")

        ele = driver.find_element(By.XPATH, "/html/body/div[2]/div")
        ele.upload_by_drop(__file__)

        ele = driver.find_element(By.XPATH, "/html/body/div[2]/div")
        text = ele.text
        assert "上传成功" in text
