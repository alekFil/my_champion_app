import os

import joblib
import streamlit as st

from inference import evaluate_element, recommend_elements
from scripts.ui import (
    add_new_unit,
    show_segment,
    show_statistic,
    show_tournament,
    show_unit_history,
)

# Определение текущей рабочей директории
current_directory = os.getcwd()

# Путь к файлу joblib
joblib_path = os.path.join(current_directory, "data/test/data.joblib")

# Загрузка данных
data = joblib.load(joblib_path)

# Streamlit приложение
st.title("My Champion App")


# Выбор спортсмена со значением по умолчанию
default_unit_id = "Спортсмен не выбран"
no_unit_id = "Спортсмена нет в списке, но имеется история его выступлений"
no_data = "Спортсмена нет в списке и не имеется истории его выступлений"
unit_id = st.selectbox(
    "Выберите спортсмена",
    [default_unit_id] + [no_unit_id] + [no_data] + list(data["unit_id"].unique()),
    index=0,
    key="unit_selectbox",
)

# Управление интерфейсом
if unit_id == default_unit_id:
    st.session_state.show_unit_history = False
    st.session_state.show_statistic = False
    st.session_state.show_unit_app = False
    st.session_state.show_upload_section = False
elif unit_id == no_unit_id:
    st.session_state.show_unit_history = False
    st.session_state.show_statistic = False
    st.session_state.show_unit_app = False
    st.session_state.show_upload_section = True
elif unit_id == no_data:
    st.session_state.show_unit_history = False
    st.session_state.show_statistic = True
    st.session_state.show_unit_app = True
    st.session_state.show_upload_section = False
else:
    st.session_state.show_unit_history = True
    st.session_state.show_statistic = False
    st.session_state.show_unit_app = True
    st.session_state.show_upload_section = False

features = {}

# Загрузка данных нового спортсмена
if st.session_state.show_upload_section:
    st.subheader("Загрузите историю соревнований нового спортсмена")
    uploaded_file = st.file_uploader("Выберите файл CSV", type="csv")
    if uploaded_file is not None:
        add_new_unit(uploaded_file)

# Отображение истории спортсмена
if st.session_state.show_unit_history:
    st.write("История выступления спортсмена на последнем соревновании")
    features["statistic"] = show_unit_history(unit_id, data)

# Выбор агрегированных характеристик
if st.session_state.show_statistic:
    st.subheader("Ручной ввод данных о спортсмене для анализа")
    features["statistic"] = show_statistic()

# Оценка исполнения элементов - основной функционал
if st.session_state.show_unit_app:
    st.subheader("Оценка исполнения элементов")
    # Добавить валидацию
    features["element"] = st.text_input(
        "Укажите элемент фигурного катания для оценки "
        "(одиночный или каскад/комбинацию). Например, 1A+2F"
    )

    features["tournament"] = show_tournament()

    features["segment"] = show_segment()

    # Главная кнопка
    if st.button("Оценить"):
        if features["element"]:
            performance_prob, errors, score = evaluate_element(features)

            st.markdown(
                f'<div style="padding:10px;background-color:#FCE4D6;border-radius:5px;">'
                f'<b>Вероятность идеального исполнения элемента:</b> <span style="color:green;font-size:16px;font-weight: bold;">{performance_prob*100:.2f}%</span>'
                f"</div>"
                f"<br>",
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div style="padding:10px;background-color:#FCE4D6;border-radius:5px;">'
                "<b>Вероятности ошибок:</b>"
                "</div>"
                "<br>",
                unsafe_allow_html=True,
            )

            errors_types = (
                "Элемент",
                "Без ошибок",
                'Ошибка "q"',
                'Ошибка "e"',
                'Ошибка "<"',
                'Ошибка "<<"',
                'Ошибка "!"',
                'Ошибка "V"',
            )

            columns = st.columns(len(errors[0]) + 1)
            with columns[0]:
                for item in errors_types:
                    st.write(item)

            for i in range(1, len(errors[0]) + 1):
                with columns[i]:
                    st.markdown(f"<b>{errors[0][i - 1]}</b>", unsafe_allow_html=True)
                    for k in range(1, 8):
                        st.write(errors[k][i - 1])

            st.markdown(
                f'<div style="padding:10px;background-color:#FCE4D6;border-radius:5px;">'
                f'<b>Прогнозируемое количество очков:</b> <span style="color:green;font-size:16px;font-weight: bold;">{score}</span>'
                f"</div>"
                f"<br>",
                unsafe_allow_html=True,
            )

            recommended_elements = recommend_elements()
            st.subheader(
                "Рекомендуемые элементы, которые могут быть выполнены идеально "
                "и принесут аналогичное количество очков или больше (в разработке):"
            )
            columns = st.columns(len(recommended_elements))
            for i, element in enumerate(recommended_elements):
                with columns[i]:
                    st.markdown(
                        f'<div style="display:flex;justify-content:center;padding:10px;background-color:#f0f0f5;border-radius:5px;">'
                        f'<span style="color:green;font-size:16px">{element}</span>'
                        f"</div>",
                        unsafe_allow_html=True,
                    )
        else:
            st.write("Укажите элемент для оценки")
