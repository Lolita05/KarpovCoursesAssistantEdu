# tests/test_step_4_servicing.py

import numpy as np
import pytest
from tasks.step_4_servicing.query_service import cosine_similarity, find_top_k
from unittest.mock import Mock, patch

# Патчим OpenAI клиент до импорта модуля
mock_response = Mock()
mock_response.data = [{"embedding": [1, 2, 3]}]

@patch("openai.OpenAI")
def test_find_top_k_real_similarity(mock_openai_class):
    """
    Тест проверяет, что функция find_top_k возвращает топ-k чанков, которые имеют наибольшее сходство
    с фиктивным эмбеддингом запроса.
    """
    # Создаем мок для ответа с правильной структурой
    mock_embedding = Mock()
    mock_embedding.embedding = [1, 2, 3]
    
    mock_response = Mock()
    mock_response.data = [mock_embedding]
    
    # Настраиваем мок для клиента
    mock_client = Mock()
    mock_client.embeddings.create.return_value = mock_response
    mock_openai_class.return_value = mock_client
    
    # Импортируем функцию после настройки мока
    from tasks.step_4_servicing.query_service import find_top_k
    
    # Фиктивные данные: создадим три чанка с эмбеддингами, размерностью 3.
    embeddings_list = [
        ("курс Аналитик Данных", [1, 2, 3]),
        ("курс HardML", [0.9, 1.8, 2.7]),
        ("Guitar lessons for beginners", [100, 100, 100]),
    ]

    user_query = "Хочу курс по ML"
    top_k = 2

    # Вызываем функцию
    result = find_top_k(user_query, embeddings_list, k=top_k, model_name="text-embedding-ada-002")

    # Ожидаем, что результат — список длиной top_k
    assert isinstance(result, list), "Функция должна возвращать список."
    assert len(result) == top_k, f"Ожидается {top_k} элементов, получено {len(result)}."

    # Рассчитаем косинусное сходство вручную для проверки:
    query_vec = np.array([1, 2, 3])
    # Для первого чанка:
    vec1 = np.array([1, 2, 3])
    score1 = np.dot(query_vec, vec1) / (np.linalg.norm(query_vec)*np.linalg.norm(vec1))  # Должно быть 1.0
    # Для второго чанка:
    vec2 = np.array([0.9, 1.8, 2.7])
    score2 = np.dot(query_vec, vec2) / (np.linalg.norm(query_vec)*np.linalg.norm(vec2))  # Должно быть 1.0, так как vec2 пропорционален vec1
    # Для третьего чанка:
    vec3 = np.array([100, 100, 100])
    score3 = np.dot(query_vec, vec3) / (np.linalg.norm(query_vec)*np.linalg.norm(vec3))  # Это значение меньше (примерно 0.186)

    # Проверяем, что первые два чанка имеют наибольшее сходство.
    # Результат должен быть отсортирован по убыванию сходства, т.е. топовый должен быть тот, у которого сходство равно ~1.0.
    top_chunk_text, top_chunk_score = result[0]
    second_chunk_text, second_chunk_score = result[1]
    
    # Проверяем, что оба топовых чанка имеют сходство, близкую к 1.0.
    assert np.isclose(top_chunk_score, 1.0, atol=1e-3), f"Ожидается сходство около 1.0, получено {top_chunk_score}"
    assert np.isclose(second_chunk_score, 1.0, atol=1e-3), f"Ожидается сходство около 1.0, получено {second_chunk_score}"

    # Также можно проверить, что 'Guitar lessons for beginners' не входит в топ-2.
    top_texts = [text for text, score in result]
    assert "Guitar lessons for beginners" not in top_texts, "Неподходящий чанк не должен входить в топ-k."

# ТЕСТЫ ДЛЯ cosine_similarity

def test_cosine_similarity_basic():
    # Два идентичных вектора должны иметь сходство 1.
    vec = [1, 2, 3]
    score = cosine_similarity(vec, vec)
    assert np.isclose(score, 1.0), f"Ожидается сходство 1, получено {score}"

def test_cosine_similarity_orthogonal():
    # Если два вектора ортогональны, то сходство должно быть 0.
    vec_a = [1, 0, 0]
    vec_b = [0, 1, 0]
    score = cosine_similarity(vec_a, vec_b)
    assert np.isclose(score, 0.0), f"Ожидается сходство 0, получено {score}"

def test_cosine_similarity_known_result():
    # Проверим на конкретном примере
    vec_a = [1, 2, 3]
    vec_b = [4, 5, 6]
    # Вычисляем вручную:
    # dot = 1*4 + 2*5 + 3*6 = 4+10+18 = 32
    # norm(a) = sqrt(1+4+9)= sqrt(14)
    # norm(b) = sqrt(16+25+36)= sqrt(77)
    # Ожидаемое сходство = 32/(sqrt(14)*sqrt(77))
    expected = 32 / (np.sqrt(14) * np.sqrt(77))
    score = cosine_similarity(vec_a, vec_b)
    assert np.isclose(score, expected), f"Ожидается {expected}, получено {score}"