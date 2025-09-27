# infrastructure/utils/selenium_driver.py
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from typing import Callable

class SeleniumDriver:
    """
    Wrapper para WebDriver do Selenium, encapsulando ações comuns
    como clicar, digitar, selecionar, aguardar elementos e captchas.
    """

    def __init__(self, driver, error_handler: Callable[[Exception], None] = None):
        """
        :param driver: instância de Selenium WebDriver
        :param error_handler: função callback para tratamento de erro (opcional)
        """
        self.driver = driver
        self.error_handler = error_handler or (lambda e: print(f"Erro Selenium: {e}"))

    # ==========================
    # Ações básicas
    # ==========================
    def clicar(self, path: str, method: str = "XPATH"):
        while True:
            try:
                element = self._find(path, method)
                if element:
                    element.click()
                    break
                sleep(0.2)
            except Exception as e:
                self.error_handler(e)
                sleep(0.5)

    def digitar(self, path: str, text: str, method: str = "XPATH"):
        while True:
            try:
                element = self._find(path, method)
                if element:
                    self._digitar(element, text)
                    break
                sleep(0.2)
            except Exception as e:
                self.error_handler(e)
                sleep(0.5)

    def digitar_blur(self, path: str, text: str, method: str = "XPATH"):
        while True:
            try:
                element = self._find(path, method)
                if element:
                    element.send_keys(text)
                    element.send_keys(Keys.TAB)
                    break
                sleep(0.2)
            except Exception as e:
                self.error_handler(e)
                sleep(0.5)

    def selecionar(self, path: str, option: str, method: str = "XPATH"):
        while True:
            try:
                element = self._find(path, method)
                if element:
                    Select(element).select_by_value(option)
                    break
                sleep(0.2)
            except Exception as e:
                self.error_handler(e)
                sleep(0.5)

    def aguardar(self, path: str, method: str = "XPATH", captcha: bool = False):
        if captcha:
            self._aguardar_captcha(path)
        else:
            while True:
                try:
                    element = self._find(path, method)
                    if element:
                        break
                    sleep(0.2)
                except Exception as e:
                    self.error_handler(e)
                    sleep(0.5)

    def elemento_no_iframe(self, iframe_xpath: str, elemento_xpath: str):
        try:
            iframe = self.driver.find_element(By.XPATH, iframe_xpath)
            self.driver.switch_to.frame(iframe)
            elemento = self.driver.find_element(By.XPATH, elemento_xpath)
            self.driver.switch_to.default_content()
            return elemento
        except Exception as e:
            self.error_handler(e)
            self.driver.switch_to.default_content()
            return None

    def click_js(self, path: str):
        element = self.driver.find_element(By.XPATH, path)
        self.driver.execute_script("arguments[0].click();", element)

    def press_tab(self, element):
        element.send_keys(Keys.TAB)

    def digitar_por_elemento(self, element, text):
        element.send_keys(text)

    # ==========================
    # Métodos privados
    # ==========================
    def _find(self, path: str, method: str):
        if method == "CSS_SELECTOR":
            return self.driver.find_element(By.CSS_SELECTOR, path)
        return self.driver.find_element(By.XPATH, path)

    def _digitar(self, element, text: str):
        return element.send_keys(text)

    def _aguardar_captcha(self, iframe_xpath: str):
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, iframe_xpath))
        while True:
            checkbox = self.driver.find_element(By.ID, "recaptcha-anchor")
            if checkbox.get_attribute("aria-checked") == "true":
                break
            sleep(0.5)
        self.driver.switch_to.default_content()
