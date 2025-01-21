import time
from typing import Optional
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def parse_karpov_landing(url: str, headless: bool = True) -> str:
    """
    Открывает указанный URL с помощью selenium-stealth и возвращает
    текст со страницы (лендинга).

    Args:
        url: URL для парсинга
        headless: Запуск в безголовом режиме

    Returns:
        str: Извлечённый текст страницы
    """
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--start-maximized')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
    
    try:
        driver = webdriver.Chrome(options=options)
        
        if headless:
            stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
            )
        
        driver.get(url)
        
        # Ждем загрузки body
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        page_html = driver.page_source
        soup = BeautifulSoup(page_html, "html.parser")
        
        # Удаляем скрипты и стили
        for element in soup(["script", "style"]):
            element.decompose()
            
        text = soup.get_text(separator=" ").strip()
        return text
        
    except Exception:
        return ""
        
    finally:
        try:
            driver.quit()
        except:
            pass
