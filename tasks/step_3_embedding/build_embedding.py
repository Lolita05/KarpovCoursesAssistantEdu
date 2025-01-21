import openai

def create_embeddings(chunks, model_name="text-embedding-ada-002"):
    """
    Создает эмбеддинги для каждого чанка текста.
    """
    client = openai.OpenAI()  # Создаем клиент здесь
    result = []
    for ch in chunks:
        response = client.embeddings.create(input=ch,
                                          model=model_name)
        result.append((ch, response.data[0].embedding))
    return result