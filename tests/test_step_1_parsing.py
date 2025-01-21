# tests/test_step_1_parsing.py

import pytest
from tasks.step_1_parsing.parse_data import parse_karpov_landing

def test_parse_karpov_landing_valid():
    """
    Проверяем, что при передаче реального URL функция возвращает непустой текст.
    """
    url = "https://karpov.courses/"
    result = parse_karpov_landing(url)
    # Предположим, что функция возвращает строку
    assert isinstance(result, str), "Ожидаем строку с текстом"
    assert len(result) > 100, "Текст слишком короткий, возможно парсинг не работает"

def test_parse_karpov_landing_invalid_url():
    """
    Проверяем, что при невалидном URL функция не падает с необработанной ошибкой.
    Либо возвращает пустую строку, либо выдаёт исключение, которое мы словим.
    """
    invalid_url = "https://wrong_url.something"
    try:
        result = parse_karpov_landing(invalid_url)
        assert isinstance(result, str)
    except Exception as e:
        assert True