import numpy as np
import openai

def cosine_similarity(vec_a, vec_b):
    """
    Вычисляет косинусное сходство двух векторных представлений.
    """
    a = np.array(vec_a)
    b = np.array(vec_b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_top_k(query: str, embeddings_list: list, k: int = 3, model_name: str = "text-embedding-ada-002"):
    """
    Находит топ-k релевантных чанков для заданного пользовательского запроса.

    :param query: Вопрос пользователя (строка).
    :param embeddings_list: Список (chunk_text, chunk_vector).
    :param k: Число релевантных чанков для возврата.
    :param model_name: Модель эмбеддингов для генерации вектора запроса.
    :return: Список (chunk_text, score).
    """
    # Эмбеддинг запроса
    response = openai.embeddings.create(input=query,
    model=model_name)
    query_vec = response.data[0].embedding

    # Подсчёт сходства
    scored_chunks = []
    for chunk_text, chunk_vec in embeddings_list:
        score = cosine_similarity(query_vec, chunk_vec)
        scored_chunks.append((chunk_text, score))

    # Сортируем по убыванию сходства
    scored_chunks.sort(key=lambda x: x[1], reverse=True)
    return scored_chunks[:k]

def generate_answer(context_chunks: list, user_query: str, model_name: str = "gpt-3.5-turbo") -> str:
    """
    Формирует ответ на основе контекста (чанков) и вопроса пользователя,
    используя ChatCompletion.

    :param context_chunks: Список чанков, которые послужат контекстом.
    :param user_query: Вопрос пользователя (строка).
    :param model_name: Название модели OpenAI ChatCompletion.
    :return: Ответ от модели (строка).
    """
    context = "\n".join(context_chunks)
    prompt = f"""Вот релевантные описания курсов Karpov.Courses:
    {context}
    На основе этих данных ответь на вопрос пользователя:
    {user_query}"""

    completion = openai.chat.completions.create(model=model_name,
    messages=[{"role": "user", "content": prompt}])
    answer = completion.choices[0].message.content
    return answer