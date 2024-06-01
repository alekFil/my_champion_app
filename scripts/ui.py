from datetime import datetime

import streamlit as st


# Функция для отображения истории элементов спортсмена
def show_unit_history(unit_id, data):
    features = {}
    last_tournament = (
        data[data["unit_id"] == unit_id]["date_start"]
        .sort_values(ascending=False)
        .unique()[0]
    )
    unit_data = data[
        (data["unit_id"] == unit_id) & (data["date_start"] == last_tournament)
    ][
        [
            "tournament_id",
            # "date_start",
            "title",
            "goe",
            "avg_score",
            "segment_name",
        ]
    ]

    st.dataframe(unit_data, height=250, width=999)

    features["color"] = data[data["unit_id"] == unit_id]["color"].iloc[-1]
    features["school_id"] = data[data["unit_id"] == unit_id]["school_id"].iloc[-1]
    features["avg_overall_place_last_year"] = data[data["unit_id"] == unit_id][
        "avg_overall_place_last_year"
    ].iloc[-1]
    features["avg_overall_total_score_last_year"] = data[data["unit_id"] == unit_id][
        "avg_overall_total_score_last_year"
    ].iloc[-1]
    features["avg_place_last_year"] = data[data["unit_id"] == unit_id][
        "avg_place_last_year"
    ].iloc[-1]
    features["avg_total_score_last_year"] = data[data["unit_id"] == unit_id][
        "avg_total_score_last_year"
    ].iloc[-1]
    features["avg_elements_score_last_year"] = data[data["unit_id"] == unit_id][
        "avg_elements_score_last_year"
    ].iloc[-1]
    features["avg_components_score_last_year"] = data[data["unit_id"] == unit_id][
        "avg_components_score_last_year"
    ].iloc[-1]
    features["avg_decreasings_score_last_year"] = data[data["unit_id"] == unit_id][
        "avg_decreasings_score_last_year"
    ].iloc[-1]
    features["avg_falls_last_year"] = data[data["unit_id"] == unit_id][
        "avg_falls_last_year"
    ].iloc[-1]

    return features


# Функция для добавления нового спортсмена
def add_new_unit(file):
    st.success(
        "История соревнований нового спортсмена успешно добавлена (в разработке)!"
    )


def show_statistic():
    features = {}
    columns = st.columns(2)
    with columns[0]:
        features["color"] = st.selectbox(
            "Категория спортсмена", options=["green", "lime"]
        )
    with columns[1]:
        features["school_id"] = st.number_input("ID школы", min_value=0, format="%i")

    st.write("##### Агрегированные характеристики спортсмена за прошлый год")
    columns = st.columns(4)
    with columns[0]:
        features["avg_overall_place_last_year"] = st.number_input(
            "Среднее место в&nbsp;соревнованиях", min_value=0.0, format="%.2f"
        )
        features["avg_overall_total_score_last_year"] = st.number_input(
            "Средний балл в&nbsp;соревнованиях", min_value=0.0, format="%.2f"
        )
    with columns[1]:
        features["avg_place_last_year"] = st.number_input(
            "Среднее место в&nbsp;программе", min_value=0.0, format="%.2f"
        )
        features["avg_total_score_last_year"] = st.number_input(
            "Средний балл в&nbsp;программе", min_value=0.0, format="%.2f"
        )
    with columns[2]:
        features["avg_elements_score_last_year"] = st.number_input(
            "Средний балл за&nbsp;элементы", min_value=0.0, format="%.2f"
        )
        features["avg_components_score_last_year"] = st.number_input(
            "Средний балл за&nbsp;артистизм", min_value=0.0, format="%.2f"
        )
    with columns[3]:
        features["avg_decreasings_score_last_year"] = st.number_input(
            "Средние количество штрафных баллов", min_value=0.0, format="%.2f"
        )
        features["avg_falls_last_year"] = st.number_input(
            "Среднее количество падений", min_value=0.0, format="%.2f"
        )
    return features


def show_tournament():
    features = {}
    st.write("Укажите характеристики соревнования")
    columns = st.columns(3)
    with columns[0]:
        features["date_start"] = st.date_input("Дата начала", datetime.now())
    with columns[1]:
        features["date_end"] = st.date_input("Дата окончания", datetime.now())
    with columns[2]:
        features["origin_id"] = st.selectbox("Место проведения", options=[0, 1, 2])
    return features


def show_segment():
    features = {}
    features["segment_name"] = st.selectbox(
        "Укажите характеристики выступления: программу",
        options=["Произвольная программа", "Короткая программа"],
    )
    features["multiply"] = st.checkbox(
        "Элемент будет выполнен во второй половине программы", False
    )
    return features
