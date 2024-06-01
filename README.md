# Разработка модели машинного обучения для прогнозирования рисков для здоровья беременных

* **Обобщенный блокнот-отчет о работе:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alekFil/maternal_health_risk/blob/main/notebooks/maternal-health-risk.ipynb)

* **Демонстрация приложения**: [My Champion App](https://my-champion-app.streamlit.app/)
 <img src="images\maternal-health-risk.streamlit.app.gif" alt="covers">


## Описание работы

**Цель работы:**
Построить и обучить модели машинного обучения (МО), позволяющие предсказать элементы фигурного катания, которые может выполнить спортсмен.

**Планируемое использование результата работы:**
Заказчику необходимо приобрести инструмент, который поможет тренеру оперативно оценить возможности и перспективы спортсмена. Кроме того, возможно использование инструмента в оценке риска получения спортсменов травм в результате совершения ошибок при исполнении элементов фигурного катания.

**Входные данные:**
Заказчик предоставил набор данных о выступлениях спортсменов на различных соревнованиях за 3 года с указанием выполненных элементов, допущенных ошибок и результатах выступлений.

## Инструменты
- **Scikit-learn**: Для создания и обучения модели.
- **PyTorch, transformers**: Для применения минимальных техник NLP в анализе элементов фигурного катания.
- **Pandas**, **Matplotlib**, **Seaborn**: Для анализа данных и визуализации.
- **Streamlit**: Для разработки и развёртывания интерактивного веб-приложения.

## Основные этапы и результаты
- **Изучение данных, предобработка, feature engineering:** В условиях ограниченности времени работы над задачей проведен быстрый исследовательский анализ данных, совмещенный с их предобработкой. Созданы новые признаки, характеризующие спортсменов на основании истории их выступлений.

- **Описание разрабатываемых моделей:** 
  
  На основании интерпретации задачи, представленной выше, принято решение о реализации четырех моделей машинного обучения:
  - *Модель № 1* для предсказания вероятности идеального исполнения элементов. Решена задача бинарной классификации (1 - идеальное исполнение, 0 - исполнение с ошибками) с определением вероятности отнесения экземпляра к одному из классов. Предсказания модели используются в работе следующей модели. Для учета качества предсказания класса 0 выбрана метрика **F1_Weighted**. Результат моделирования **F1 = 0.84**.
  - *Модель № 2* для предсказания количества очков, которые спортсмен может получить за выполнение элемента (идеальное или с ошибками) - GOE. Решена задача регрессии. Предсказания модели используются в работе следующей модели и расчете общей суммы очков за исполнение элемента. Для анализа моделей регрессии выбрана метрика RMSE, отражающая среднюю ошибку предсказания в единицах измерения таргета. Результат моделирования **RMSE = 0.57** для оценок GOE в диапазоне [-5,5].
  - *Модель № 3* для предсказания вероятности возникновения ошибок. Решена задача мульти-лейбл классификации для 7 ошибок ("q", "e", "!", "<", "<<", "V"; для прогнозирования иных ошибок, например, nS, nU и др. определено, что не достаточно данных) с определением вероятности присвоения меток классам. Для анализа моделей мульти-лейбл классификации выбрана метрика **Hamming Loss**, отражающая долю меток, которые были предсказаны неправильно. 
  - *Модель № 4* (планируется к реализации, эксперименты не показали качественных результатов) для предсказания элементов фигурного катания, которые могут быть исполнены идеально и принести равное или большее количество очков.

- **Проверка моделей на тестовых данных:** 
  Планируется провести оценку качество моделей на эмпирических тестовых данных. Изучить ошибки моделей. Последний этап не завершен ввиду ограниченности времени.

## Выводы
...In progress

## Запуск проекта
Чтобы развернуть проект необходимо:
1. Клонировать репозиторий:
`git clone https://github.com/alekFil/maternal_health_risk.git`
2. Установить зависимости: `pip install -r requirements.txt`

Запуск Streamlit приложения: 
```bash
streamlit run app.py
```

## Запуск ноутбуков
Чтобы запустить ноутбуки необходимо установить иные зависимости:
1. Клонировать репозиторий:
`git clone https://github.com/alekFil/maternal_health_risk.git`
2. Установить зависимости для ноутбуков: `pip install -r requirements-notebooks.txt`

## Контакты
Автор проекта - Алексей Филатов: [telegram @alekFil](https://t.me/alekfil).