import operator
from functools import reduce

import joblib  # noqa: F401

from scripts.feature_preprocessing import feature_preprocessing, get_score

models_path = {
    "one": "models/model_one.joblib",  # Модель для прогнозирования идеального исполнения
    "two": "models/model_two.joblib",  # Модель для прогнозирования GOE
    "three": "models/model_three.joblib",  # Модель для прогнозирования ошибок
    "four": "models/model_four.joblib",  # Модель рекомендательной системы
}


# Функция для оценки элемента
def evaluate_element(features, models_path=models_path):
    features["target_clear"] = None
    features["goe"] = None
    features_one = feature_preprocessing(features, model="one")
    model_one = joblib.load(models_path["one"])
    performance_probs = model_one.predict_proba(features_one)[:, 1]
    performance_prob = reduce(operator.mul, performance_probs)

    features["target_clear"] = list(map(round, performance_probs))
    features_two = feature_preprocessing(features, model="two")
    model_two = joblib.load(models_path["two"])
    scores = model_two.predict(features_two)

    features["goe"] = scores
    features_three = feature_preprocessing(features, model="three")
    model_three = joblib.load(models_path["three"])
    errors_probs = model_three.predict_proba(features_three)
    errors_prob = [map(lambda val: round(val, 3), x[:, 1]) for x in errors_probs]
    errors = {
        0: features["element"].split("+"),
        1: list(errors_prob[0]),
        2: list(errors_prob[1]),
        3: list(errors_prob[2]),
        4: list(errors_prob[3]),
        5: list(errors_prob[4]),
        6: list(errors_prob[5]),
        7: list(errors_prob[6]),
    }

    score = get_score(features["element"], errors, scores)

    if score < 0:
        score = "Что-то пошло не так, проверьте элемент"

    return performance_prob, errors, score


# Функция для рекомендации элементов
def recommend_elements(models_path=models_path):
    # Здесь должна быть логика для рекомендации элементов
    return ["1A", "2Lz", "3F", "4Lo"]
