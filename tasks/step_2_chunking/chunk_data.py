def chunk_text(text: str, chunk_size: int = 800) -> list:
    """
    Делит большой текст на более мелкие чанки (по chunk_size символов).

    :param text: Исходный текст.
    :param chunk_size: Предельный размер чанка (по количеству символов или условных 'токенов').
    :return: Список строк (чанков).
    """
    tokens = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for token in tokens:
        current_chunk.append(token)
        current_length += len(token) + 1  # +1 на пробел
        if current_length >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0

    # Добавляем последний чанк, если остался
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks