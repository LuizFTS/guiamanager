from typing import Callable, Optional
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError, Page, Browser, Playwright, async_playwright
import asyncio
import os

class PlaywrightDriver:
    """
    Wrapper para Playwright Page com ações básicas de interação e suporte a reCAPTCHA.
    """

    def __init__(self, error_handler: Optional[Callable[[Exception], None]] = None):
        self.error_handler = error_handler or (lambda e: print(f"Erro Playwright: {e}"))

        self.page: Optional[Page] = None
        self.browser: Optional[Browser] = None
        self.playwright: Optional[Playwright] = None

    async def async_init(self, headless: bool = True):
        """
        Inicialização assíncrona do Playwright, browser e page.
        Retorna self para permitir factory pattern.
        """
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.context = await self.browser.new_context(accept_downloads=True)
        self.page = await self.context.new_page()
        return self

    async def waitDownload(self, path: str, frame_name: str | None = None, path_download: str = None, file_download: str = None):

        async with self.page.expect_download() as download_info:
            await self.clicar(path, frame_name=frame_name)  # botão que gera o PDF

        download = await download_info.value

        # Nome e caminho final
        final_path = os.path.join(path_download, file_download)

        # Salva o arquivo no local desejado
        await download.save_as(final_path)

        print("PDF salvo em:", final_path)

        await self.browser.close()


    # ==========================
    # Utilitário interno
    # ==========================
    async def _find(self, xpath: str, timeout: int = 5000):
        """
        Aguarda e retorna o elemento localizado pelo XPATH.
        """
        try:
            return await self.page.wait_for_selector(f"xpath={xpath}", timeout=timeout)
        except PlaywrightTimeoutError as e:
            self.error_handler(e)
            return None

    # ==========================
    # Funções solicitadas
    # ==========================
    async def clicar(self, element_xpath: str, frame_name: str | None = None):
        try:
            locator = (
                self.page.frame_locator(f"frame[name='{frame_name}']").locator(element_xpath)
                if frame_name else
                self.page.locator(element_xpath)
            )

            await locator.first.wait_for(state="visible")
            await locator.first.click()

        except Exception as e:
            self.error_handler(e)

    async def digitar(self, element_xpath: str, texto: str, limpar: bool = True, frame_name: str | None = None):
        try:
            if frame_name:
                locator = self.page.frame_locator(f"frame[name='{frame_name}']").locator(element_xpath)
            else:
                locator = self.page.locator(element_xpath)

            if await locator.count() > 0:
                if limpar:
                    await locator.fill("")
                await locator.type(texto)
            else:
                raise Exception(f"Elemento não encontrado: {element_xpath}")
        except Exception as e:
            self.error_handler(e)

    async def digitar_blur(self, element_xpath: str, texto: str, limpar: bool = True, frame_name: str | None = None):
        try:
            if frame_name:
                locator = self.page.frame_locator(f"frame[name='{frame_name}']").locator(element_xpath)
            else:
                locator = self.page.locator(element_xpath)

            if await locator.count() > 0:
                if limpar:
                    await locator.fill("")
                await locator.type(texto)
                await locator.evaluate("el => el.blur()")
            else:
                raise Exception(f"Elemento não encontrado: {element_xpath}")
        except Exception as e:
            self.error_handler(e)

    async def selecionar(self, element_xpath: str, option: str, frame_name: str | None = None):
        """
        Seleciona uma opção de um elemento <select> pelo valor.
        """
        try:
            if frame_name:
                locator = self.page.frame_locator(f"frame[name='{frame_name}']").locator(element_xpath)
            else:
                locator = self.page.locator(element_xpath)
            
            if await locator.count() > 0:
                await locator.select_option(value=option)
        except Exception as e:
            self.error_handler(e)

    async def aguardar(self, element_xpath: str, timeout: int = 5000) -> bool:
        """
        Aguarda o elemento ficar visível.
        """
        try:
            await self.page.wait_for_selector(f"xpath={element_xpath}", state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    async def click_js(self, element_xpath: str):
        """
        Clica no elemento usando JavaScript.
        """
        try:
            await self.page.evaluate(
                """(xpath) => {
                    const el = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    if (el) el.click();
                }""",
                element_xpath
            )
        except Exception as e:
            self.error_handler(e)

    async def aguardar_captcha(self, timeout: int = 10):
        """
        Aguarda o iframe do reCAPTCHA, entra no frame, clica no checkbox e aguarda validação.
        """
        try:
            # Aguarda container do captcha
            await self.page.wait_for_selector("css=div[name='captcha'][vc-recaptcha]", timeout=timeout * 1000)

            # Aguarda iframe do captcha
            iframe_element = await self.page.wait_for_selector(
                "css=div[name='captcha'][vc-recaptcha] iframe",
                timeout=timeout * 1000
            )
            iframe = await iframe_element.content_frame()

            # Clica no checkbox
            checkbox = await iframe.wait_for_selector("#recaptcha-anchor", timeout=timeout * 1000)
            await checkbox.click()

            # Aguarda até que aria-checked seja "true"
            await iframe.wait_for_selector(
                '#recaptcha-anchor[aria-checked="true"]',
                timeout=300 * 1000
            )
        except Exception as e:
            self.error_handler(e)


    async def press(self, element_xpath: str, key: str):
        """
        Pressiona uma tecla em um elemento específico (ex: 'Enter', 'Tab', 'End').
        """
        try:
            element = await self._find(element_xpath)
            if element:
                await element.press(key)
        except Exception as e:
            self.error_handler(e)


    async def close(self):
        """
        Fecha a página, o browser e o Playwright.
        """
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()