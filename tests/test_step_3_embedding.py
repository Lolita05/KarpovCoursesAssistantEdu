# tests/test_step_3_embedding.py

import pytest
from tasks.step_3_embedding.build_embedding import create_embeddings

def test_create_embeddings_basic():
    """
    Проверяем, что функция возвращает список кортежей (text, vector),
    и что vector не пустой.
    """
    sample_chunks = ["Hello World", "Data Science is fun"]
    embeddings_list = create_embeddings(sample_chunks)
    
    assert len(embeddings_list) == len(sample_chunks), "Количество результатов не совпадает с количеством чанков."
    
    for (text, vec), original_text in zip(embeddings_list, sample_chunks):
        # проверяем, что text совпадает
        assert text == original_text, "Текст чанка не совпадает с исходным."
        # проверяем, что vector - не пустой
        assert vec is not None, "Пустой вектор эмбеддинга."

        if hasattr(vec, "__len__"):
            assert len(vec) > 0, "Вектор не должен быть длины 0."