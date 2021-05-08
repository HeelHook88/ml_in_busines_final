# Курс Машинное обучение в бизнесе

# Итоговый проект

### Стек:
pandas, sklearn, numpy, flask, lightgbm


Данные: https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Coimbra

Задача: предсказать Рак молочной железы

Целевая переменная: target

Используемые признаки:

* Age(int64)
* BMI(float64) 
* Glucose(int64)
* Insulin(float64)
* HOMA(float64)
* Leptin(float64)
* Adiponectin(float64)
* Resistin(float64)
* MCP(float64)


Модель: lightgbm

Клонируем репозиторий и создаем образ

$ git clone https://github.com/HeelHook88/ml_in_busines_final.git
$ cd ml_in_busines_final
$ $ docker build -t flask_app/ 

Запускаем контейнер

Здесь Вам нужно создать каталог локально и сохранить туда предобученную модель (<your_local_path_to_pretrained_models> нужно заменить на полный путь к этому каталогу)

Предобученная модель лежит в \flask_app\model

$ docker run -d -p 8180:8180 -p 8181:8181 -v <your_local_path_to_pretrained_models>:/app/app/models flask_app

Переходим на 127.0.0.1:8180
