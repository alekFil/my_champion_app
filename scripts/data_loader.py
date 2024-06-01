import os

import joblib

# Определение текущей рабочей директории
current_directory = os.getcwd()

# Путь к файлу joblib
joblib_path = os.path.join(current_directory, "data/processed/data.joblib")


def load_data():
    # Загрузка данных
    data = joblib.load(joblib_path)
    data = data.rename(columns={"athlete_id": "unit_id"})

    return data
