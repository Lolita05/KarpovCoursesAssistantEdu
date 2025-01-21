# tests/test_step_1.py

import pytest
from unittest.mock import Mock, patch
from tasks.step_1_parsing.parse_data import parse_karpov_landing
import requests

@patch('requests.get')
def test_parse_karpov_landing_valid(mock_get):
    """
    Проверяем, что при передаче реального URL функция возвращает непустой текст.
    """
    # Подготавливаем мок-ответ
    mock_response = Mock()
    mock_response.text = """
    <html>
        <head>
            <script>var x = 1;</script>
            <style>.some-class { color: red; }</style>
        </head>
        <body>
            <h1>Karpov.Courses</h1>
            <p>Образовательная платформа</p>
            <div>Курсы по аналитике и программированию</div>
        </body>
    </html>
    """
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Вызываем функцию
    url = "https://karpov.courses"
    result = parse_karpov_landing(url)

    # Проверяем результат
    assert isinstance(result, str), "Ожидаем строку с текстом"
    assert len(result) > 0, "Текст не должен быть пустым"
    assert "Karpov.Courses" in result, "Ожидаем найти название в тексте"
    assert "var x = 1" not in result, "JavaScript код должен быть удален"
    assert "color: red" not in result, "CSS стили должны быть удалены"

    # Проверяем, что запрос был сделан с правильными параметрами
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert args[0] == url
    assert 'headers' in kwargs
    assert 'timeout' in kwargs

@patch('requests.get')
def test_parse_karpov_landing_invalid_url(mock_get):
    """
    Проверяем, что при невалидном URL функция возвращает пустую строку.
    """
    # Настраиваем мок для имитации ошибки
    mock_get.side_effect = Exception("Connection error")

    # Вызываем функцию
    invalid_url = "https://this-url-does-not-exist.something"
    result = parse_karpov_landing(invalid_url)

    # Проверяем результат
    assert isinstance(result, str), "Должна вернуться строка"
    assert result == "", "Для невалидного URL должна вернуться пустая строка"

    # Проверяем, что была попытка запроса
    mock_get.assert_called_once()

@patch('requests.get')
def test_parse_karpov_landing_http_error(mock_get):
    """
    Проверяем обработку HTTP ошибок.
    """
    # Настраиваем мок для имитации HTTP ошибки
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
    mock_get.return_value = mock_response

    # Вызываем функцию
    url = "https://karpov.courses/not-found"
    result = parse_karpov_landing(url)

    # Проверяем результат
    assert result == "", "При HTTP ошибке должна вернуться пустая строка"
