import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup


def parse_karpov_landing(url: str, headless: bool = True) -> str:
    """
    Открывает указанный URL с помощью undetected-chromedriver и возвращает
    текст со страницы (лендинга).

    :param url: URL для парсинга.
    :param headless: Запуск в безголовом режиме, если True.
    :return: Строка с извлечённым текстом страницы.
    """
    options = uc.ChromeOptions()
    if headless:
        options.headless = True

    driver = uc.Chrome(options=options, version_main=131)
    try:
        driver.get(url)
        time.sleep(3)  # Ждём, чтобы страница успела прогрузиться
        page_html = driver.page_source
    finally:
        driver.quit()

    soup = BeautifulSoup(page_html, "html.parser")
    text = soup.get_text(separator=" ")
    return text
