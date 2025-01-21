# tests/test_step_3_embedding.py

import pytest
from unittest.mock import Mock, patch

@patch("openai.OpenAI")
def test_create_embeddings_basic(mock_openai_class):
    """
    Проверяем, что функция возвращает список кортежей (text, vector),
    и что vector не пустой.
    """
    # Создаем мок для ответа с правильной структурой
    mock_embedding = Mock()
    mock_embedding.embedding = [0.1, 0.2, 0.3]
    
    mock_response = Mock()
    mock_response.data = [mock_embedding]
    
    # Настраиваем мок для клиента
    mock_client = Mock()
    mock_client.embeddings.create.return_value = mock_response
    mock_openai_class.return_value = mock_client
    
    # Импортируем функцию после настройки мока
    from tasks.step_3_embedding.build_embedding import create_embeddings
    
    sample_chunks = ["Hello World", "Data Science is fun"]
    embeddings_list = create_embeddings(sample_chunks)
    
    # Проверяем результат
    assert len(embeddings_list) == 2
    for text, vector in embeddings_list:
        assert isinstance(text, str)
        assert isinstance(vector, list)
        assert len(vector) > 0