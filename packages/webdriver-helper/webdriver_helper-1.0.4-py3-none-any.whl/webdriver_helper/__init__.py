import logging
import os
import warnings
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.options import ArgOptions as ArgOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IEService

__all__ = ["get_webdriver"]

from sys import exit, version_info

logger = logging.getLogger(__name__)

if not all([version_info.major == 3, version_info.minor >= 9]):
    msg = """
    webdriver_helper: Python version should >=3.9，
    If you need to be compatible with special scenarios,
    please contact the developer for paid customization. """
    print(msg)
    logger.critical(msg)
    exit(-1)


def get_webdriver(
    browser="chrome",
    version=None,
    options: Optional[ArgOptions] = None,
    service_args: dict = None,
) -> webdriver.Remote:
    """
    自动就绪selenium，目前只支持Chrome 和 FireFox
    1. 下载浏览器驱动
    2. 实例化Service
    3. 实例化WebDriver
    :param browser: 浏览器类型
    :param version: 浏览器版本
    :param options: 浏览器选项
    :param service_args: service 实例化的参数
    :param capabilities: grid 的启动参数
    :return:
    """
    if browser != 'chrome':
        warnings.warn(
            "只实现chromedriver下载加速，如果需要对其他driver加速，建议升级到2.*。详情咨询wx:python_sanmu",
            DeprecationWarning,
        )
    service_args = service_args or {}
    browser = browser.lower()

    if version:
        msg = "version参数已被弃用，请通过options.browser_version指定浏览器器版本。详情咨询wx:python_sanmu"
        if options:
            logging.warning(msg)
            options.browser_version = version
        raise ValueError(msg)

    if browser == "chrome":
        os.environ['SE_CHROME_MIRROR_URL'] = 'http://118.24.147.95:8086/chrome/'
        return webdriver.Chrome(
            service=ChromeService(**service_args),
            options=options,
        )
    elif browser == "edge":
        return webdriver.Edge(
            service=EdgeService(**service_args),
            options=options,
        )

    elif browser == "firefox":
        return webdriver.Firefox(
            service=FirefoxService(**service_args),
            options=options,
        )

    elif browser == "ie":
        return webdriver.Ie(
            service=IEService(**service_args),
            options=options,
        )
