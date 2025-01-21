import requests
from bs4 import BeautifulSoup
from typing import Optional

def parse_karpov_landing(url: str, headless: bool = True) -> str:
    """
    Открывает указанный URL с помощью requests и возвращает
    текст со страницы (лендинга).

    Args:
        url: URL для парсинга
        headless: Параметр оставлен для обратной совместимости

    Returns:
        str: Извлечённый текст страницы
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Делаем GET запрос
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Проверяем статус ответа
        
        # Парсим HTML
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Удаляем скрипты и стили
        for element in soup(["script", "style"]):
            element.decompose()
            
        # Получаем текст
        text = soup.get_text(separator=" ").strip()
        return text
        
    except Exception as e:
        return ""
