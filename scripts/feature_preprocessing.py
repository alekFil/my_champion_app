import os

import joblib

# Определение текущей рабочей директории
current_directory = os.getcwd()

# Путь к файлу joblib
file_path = os.path.join(current_directory, "data/mats/base_scores_dict.joblib")

if os.path.isfile(file_path):
    base_scores_dict = joblib.load(file_path)
else:
    raise FileNotFoundError("There is no scores dict")


def get_difficulty(element, multiply, base_scores_dict=base_scores_dict):
    try:
        base_score = base_scores_dict[base_scores_dict["item"] == element].iloc[0, 1]
    except IndexError:
        base_score = -1000
    max_scores = base_scores_dict["base_score"].max()

    return round(base_score * (1 + 0.1 * multiply) / max_scores, 2)


def get_processed_features(i, elements, features, model):
    tournament_duration = (
        features["tournament"]["date_end"] - features["tournament"]["date_start"]
    ).days
    start_month = features["tournament"]["date_start"].month
    start_day_of_week = features["tournament"]["date_start"].weekday()
    end_month = features["tournament"]["date_end"].month
    end_day_of_week = features["tournament"]["date_end"].weekday()
    start_is_weekend = int(start_day_of_week >= 5)
    end_is_weekend = int(end_day_of_week >= 5)
    seasons = {
        1: "зима",
        2: "зима",
        3: "весна",
        4: "весна",
        5: "весна",
        6: "лето",
        7: "лето",
        8: "лето",
        9: "осень",
        10: "осень",
        11: "осень",
        12: "зима",
    }
    multiply = int(features["segment"]["multiply"])
    start_season = seasons[features["tournament"]["date_start"].month]
    end_season = seasons[features["tournament"]["date_end"].month]
    tournament_year = features["tournament"]["date_start"].year
    falls = 0
    element = elements[i]
    if i == 0:
        prev_element = "0"
        next_element = elements[i + 1]
    elif i == len(elements) - 1:
        prev_element = elements[i - 1]
        next_element = "0"
    else:
        prev_element = elements[i - 1]
        next_element = elements[i + 1]
    difficulty = get_difficulty(element, multiply, base_scores_dict)

    if len(elements) == 1:
        single_element = 1
    else:
        single_element = 0

    if features["goe"] is not None:
        goe = features["goe"][i]
    else:
        goe = None
    if features["target_clear"] is not None:
        target_clear = features["target_clear"][i]
    else:
        target_clear = None

    features_dict = {
        0: goe,
        1: features["segment"]["segment_name"],
        2: features["statistic"]["color"],
        3: features["statistic"]["school_id"],
        4: features["tournament"]["origin_id"],
        5: multiply,
        6: tournament_duration,
        7: start_month,
        8: end_month,
        9: start_day_of_week,
        10: end_day_of_week,
        11: start_is_weekend,
        12: end_is_weekend,
        13: start_season,
        14: end_season,
        15: tournament_year,
        16: falls,
        17: features["statistic"]["avg_overall_place_last_year"],
        18: features["statistic"]["avg_overall_total_score_last_year"],
        19: features["statistic"]["avg_components_score_last_year"],
        20: features["statistic"]["avg_place_last_year"],
        21: features["statistic"]["avg_elements_score_last_year"],
        22: features["statistic"]["avg_decreasings_score_last_year"],
        23: features["statistic"]["avg_total_score_last_year"],
        24: features["statistic"]["avg_falls_last_year"],
        25: target_clear,  # one-0, two-1,
        26: difficulty,
        27: element,
        28: prev_element,
        29: "0",  # attr_prev_element
        30: next_element,
        31: "0",  # attr_next_element
        32: single_element,  # single_element
        33: 0,  # clear_prev_element
        34: 0,  # clear_next_element
        35: 1,  # perfect_attr_prev_element
        36: 0,  # q_attr_prev_element
        37: 0,  # e_attr_prev_element
        38: 0,  # l_attr_prev_element
        39: 0,  # ll_attr_prev_element
        40: 0,  # h_attr_prev_element
        41: 0,  # v_attr_prev_element
        42: 1,  # perfect_attr_next_element
        43: 0,  # q_attr_next_element
        44: 0,  # e_attr_next_element
        45: 0,  # l_attr_next_element
        46: 0,  # ll_attr_next_element
        47: 0,  # h_attr_next_element
        48: 0,  # v_attr_next_element
    }

    if model == "one":
        del features_dict[0]
        del features_dict[25]
        for i in range(35, 49):
            del features_dict[i]
    elif model == "two":
        del features_dict[0]
        for i in range(35, 49):
            del features_dict[i]
    elif model == "three":
        del features_dict[29]
        del features_dict[31]
        del features_dict[33]
        del features_dict[34]

    return list(features_dict.values())


def feature_preprocessing(features, model):
    elements = features["element"].split("+")

    all_features = []
    for i in range(0, len(elements)):
        all_features.append(get_processed_features(i, elements, features, model=model))

    return all_features


def get_score(elements, errors, scores, base_scores_dict=base_scores_dict):
    elements = elements.split("+")
    score = 0
    for i, element in enumerate(elements):
        errors_types = (
            "",
            "q",
            "e",
            "<",
            "<<",
            "!",
            "V",
        )
        for k, v in errors.items():
            if k == 0:
                continue
            if v[i] >= 0.5:
                element += errors_types[k]
        try:
            base_score = base_scores_dict[base_scores_dict["item"] == element].iloc[
                0, 1
            ]
        except IndexError:
            base_score = -1000

        score += base_score + scores[i]

    return round(score, 2)
