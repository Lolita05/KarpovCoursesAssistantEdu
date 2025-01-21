import openai

def create_embeddings(chunks: list, model_name: str = "text-embedding-ada-002") -> list:
    """
    Генерирует эмбеддинги (векторы) для списка чанков, используя OpenAI API.

    :param chunks: Список строк (чанков).
    :param model_name: Название модели эмбеддингов OpenAI (по умолчанию text-embedding-ada-002).
    :return: Список кортежей (chunk_text, embedding_vector).
    """
    results = []
    for ch in chunks:
        response = openai.embeddings.create(input=ch,
        model=model_name)
        emb = response.data[0].embedding
        results.append((ch, emb))
    return results