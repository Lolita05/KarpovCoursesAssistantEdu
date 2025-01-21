# tests/test_step_1.py

import pytest
from tasks.step_1_parsing.parse_data import parse_karpov_landing

def test_parse_karpov_landing_valid():
    """
    Проверяем, что при передаче реального URL функция возвращает непустой текст.
    """
    url = "https://karpov.courses"
    result = parse_karpov_landing(url, headless=True)
    assert isinstance(result, str), "Ожидаем строку с текстом"
    assert len(result) > 100, "Текст слишком короткий, возможно парсинг не работает"

def test_parse_karpov_landing_invalid_url():
    """
    Проверяем, что при невалидном URL функция возвращает пустую строку.
    """
    invalid_url = "https://this-url-does-not-exist.something"
    result = parse_karpov_landing(invalid_url, headless=True)
    assert isinstance(result, str), "Должна вернуться строка"
    assert result == "", "Для невалидного URL должна вернуться пустая строка"
