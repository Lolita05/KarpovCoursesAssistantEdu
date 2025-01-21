import streamlit as st
import openai
import os
from dotenv import load_dotenv
import sys

# Определяем абсолютный путь к корневой папке проекта
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
# Добавляем корневую папку в sys.path, если её там ещё нет
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from tasks.step_1_parsing.parse_data import parse_karpov_landing
from tasks.step_2_chunking.chunk_data import chunk_text
from tasks.step_3_embedding.build_embedding import create_embeddings
from tasks.step_4_servicing.query_service import find_top_k, generate_answer

# Читаем ключи OpenAI из окружения
load_dotenv()  # Загружаем переменные из .env
openai.api_key = os.getenv("OPENAI_API_KEY")

# Добавляем (и правим) CSS стили для кастомизации
st.markdown(
    """
    <style>
    /* =========================
         Main Area
       ========================= */
    /* Main background color & text color */
    [data-testid="stAppViewContainer"] {
        background-color: #272B2E !important;
        color: #E1E4E7 !important;
    }
    
    /* Container inside the main area */
    .main .block-container {
        background-color: #272B2E !important;
        color: #E1E4E7 !important;
        font-family: 'Arial', sans-serif;
    }

    /* Headers color in main area */
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] h4,
    [data-testid="stAppViewContainer"] h5,
    [data-testid="stAppViewContainer"] h6,
    .main h1,
    .main h2,
    .main h3,
    .main h4,
    .main h5,
    .main h6 {
        color: #E1E4E7 !important;
    }

    /* Filling blocks in the main area: text inputs, textareas, etc. */
    .main .block-container input[type="text"],
    .main .block-container textarea,
    .main .block-container input[type="number"],
    [data-testid="stAppViewContainer"] input[type="text"],
    [data-testid="stAppViewContainer"] textarea,
    [data-testid="stAppViewContainer"] input[type="number"] {
        background-color: #E1E4E7 !important;
        color: #272B2E !important;
        border: 1px solid #FF5533 !important;
        padding: 8px !important;
        font-size: 16px !important;
    }
    
    /* Placeholder color in main area */
    .main .block-container input::placeholder,
    .main .block-container textarea::placeholder,
    [data-testid="stAppViewContainer"] input::placeholder,
    [data-testid="stAppViewContainer"] textarea::placeholder {
        color: #272B2E !important;
    }
    
    /* Buttons in the main area */
    .stButton button {
        background-color: #FF5533 !important;
        color: #272B2E !important;
        border: none !important;
    }
    
    /* =========================
         Override for labels and markdown text in main area:
         Set text color to rose (#FFC0CB)
       ========================= */
    .main .block-container [data-testid="stMarkdownContainer"],
    .main .block-container [data-testid="stMarkdownContainer"] * {
        color: #FFC0CB !important;
        background-color: transparent !important;
    }
    
    /* Alternative: apply to common text elements inside main container */
    .main .block-container p,
    .main .block-container span,
    .main .block-container label {
        color: #FFC0CB !important;
    }
    
    /* =========================
         Sidebar
       ========================= */
    [data-testid="stSidebar"] {
        background-color: #E1E4E7 !important;
        color: #272B2E !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5,
    [data-testid="stSidebar"] h6,
    [data-testid="stSidebar"] label {
        color: #272B2E !important;
    }
    
    [data-testid="stSidebar"] input[type="text"],
    [data-testid="stSidebar"] textarea,
    [data-testid="stSidebar"] input[type="number"] {
        background-color: #ffffff !important;
        color: #272B2E !important;
        border: 1px solid #ffffff !important;
        padding: 4px 8px !important;
        font-size: 16px !important;
    }
    
    [data-testid="stSidebar"] input::placeholder,
    [data-testid="stSidebar"] textarea::placeholder {
        color: #272B2E !important;
    }
    
    [data-testid="stSidebar"] .stButton button {
        background-color: #FF5533 !important;
        color: #272B2E !important;
        border: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def colored_label_text_input(label: str, default_value: str = "", color: str = "#FF5533") -> str:
    """
    Отображает стилизованный ярлык над полем ввода и вызывает st.text_input с label_visibility="hidden".
    """
    st.markdown(
        f"<p style='margin-bottom:1px; font-size:16px; color:{color};'>{label}</p>",
        unsafe_allow_html=True
    )
    return st.text_input("", value=default_value, label_visibility="hidden")

def main():
    st.title("KarpovCourses Assistant RAG Demo")

    # Боковое меню с настройками
    st.sidebar.title("Настройки")
    headless = st.sidebar.checkbox("Безголовый режим (headless)?", value=True)
    chunk_size = st.sidebar.number_input("Размер чанка (символов)", value=800, step=100)
    k_top = st.sidebar.number_input("Сколько чанков искать?", value=3, step=1)
    model_name = st.sidebar.text_input("Модель Embeddings", value="text-embedding-ada-002")
    chat_model = st.sidebar.text_input("Модель ChatCompletion", value="gpt-3.5-turbo")

    # 1. Сбор данных
    st.header("1. Сбор (парсинг) данных")
    default_url = "https://karpov.courses/"
    url_input = colored_label_text_input("URL лендинга для парсинга", default_value=default_url, color="#FF5533")

    if st.button("Собрать данные"):
        with st.spinner("Парсим страницу..."):
            text_data = parse_karpov_landing(url_input, headless=headless)
        st.success("Парсинг завершён!")
        st.markdown(
            f'<span class="colored-text">Длина текста: {len(text_data)} символов</span>',
            unsafe_allow_html=True
        )
        st.session_state["landing_text"] = text_data

    # 2. Предобработка и чанкование
    st.header("2. Предобработка и чанкование")
    if st.button("Разбить на чанки"):
        if "landing_text" not in st.session_state:
            st.warning("Сначала необходимо спарсить страницу.")
        else:
            with st.spinner("Чанкуем текст..."):
                chunks = chunk_text(st.session_state["landing_text"], chunk_size=chunk_size)
            st.success("Чанкование завершено!")
            st.markdown(
                f'<span class="colored-text">Получено чанков: {len(chunks)}</span>',
                unsafe_allow_html=True
            )
            st.session_state["chunks"] = chunks

    # 3. Генерация эмбеддингов
    st.header("3. Генерация эмбеддингов")
    if st.button("Сгенерировать эмбеддинги"):
        if "chunks" not in st.session_state:
            st.warning("Сначала сделайте чанкование.")
        else:
            with st.spinner("Генерируем эмбеддинги..."):
                embeddings_list = create_embeddings(st.session_state["chunks"], model_name=model_name)
            st.success("Эмбеддинги сгенерированы!")
            st.session_state["embeddings_list"] = embeddings_list

    # 4. Задать вопрос
    st.header("4. Задайте вопрос ассистенту")
    user_query = colored_label_text_input("Ваш вопрос о курсах?", default_value="", color="#FF5533")

    if st.button("Получить ответ"):
        if "embeddings_list" not in st.session_state:
            st.warning("Сперва сгенерируйте эмбеддинги!")
        elif not user_query.strip():
            st.warning("Пожалуйста, введите вопрос.")
        else:
            with st.spinner("Ищем наиболее релевантные чанки..."):
                top_chunks = find_top_k(user_query, st.session_state["embeddings_list"], k=k_top, model_name=model_name)
                top_texts = [t[0] for t in top_chunks]  # извлекаем chunk_text

            with st.spinner("Обращаемся к LLM..."):
                answer = generate_answer(top_texts, user_query, model_name=chat_model)

            st.success("Ответ получен!")
            st.markdown(
                f'<span class="colored-text">{answer}</span>',
                unsafe_allow_html=True
            )


if __name__ == "__main__":
    main()