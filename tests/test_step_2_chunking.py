# tests/test_step_2_chunking.py

import pytest
from tasks.step_2_chunking.chunk_data import chunk_text

def test_chunk_text_short_input():
    """
    Если длина текста меньше chunk_size, то должен вернуться всего один чанк.
    """
    text = "Hello, this is a short text."
    chunks = chunk_text(text, chunk_size=100)
    assert len(chunks) == 1, "Ожидаем один чанк, т.к. текст короче 100 символов."

def test_chunk_text_long_input():
    """
    Проверяем, что функция корректно делит текст на чанки.
    """
    text = "Lorem ipsum " * 200  # искусственно большой текст
    # chunk_size = 300 символов
    chunk_size = 300
    chunks = chunk_text(text, chunk_size)
    
    # Проверим, что ни один чанк не превышает 300 символов
    for ch in chunks:
        assert len(ch) <= chunk_size, "Чанк превышает заданный лимит символов."
    
    # Проверим, что общий текст 'раскидался' по разным чанкам
    total_length = sum(len(ch) for ch in chunks)
    # ожидаем, что хотя бы половина исходного текста в сумме есть (чтобы убедиться, что чанкование не съедает все).
    assert total_length > len(text) * 0.5, "Слишком большая потеря текста при чанковании."

def test_chunk_text_empty_input():
    """
    Проверяем, если подали пустой текст, должна вернуться пустая структура.
    """
    chunks = chunk_text("", chunk_size=100)
    # Считаем, что если вход пустой, выход тоже пустой
    assert len(chunks) == 0 or (len(chunks) == 1 and chunks[0] == ""), \
        "При пустом тексте должны получить пустой список чанков или ['']."