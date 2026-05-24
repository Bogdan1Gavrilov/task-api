# task-api
CRUD-сервис для управления задачами. FastAPI + Docker + автодеплой
## Локальный запуск

    conda create -y -n task-api python=3.11
    conda activate task-api
    pip install -r requirements.txt
    uvicorn app.main:app --reload

- **Live demo:** https://91-197-97-107.nip.io/
- **Swagger UI:** https://91-197-97-107.nip.io/docs
- **Health-check:** https://91-197-97-107.nip.io/health

## Живой сервис

- `notebooks/wine_train.ipynb`  — обучение `DecisionTreeClassifier` на `sklearn.datasets.load_wine` с label noise 15% в train, подбор регуляризации (`max_depth=4`) через `GridSearchCV`. Регуляризация поднимает test accuracy с 0.76 (baseline) до 0.82 и сжимает train/test gap с 0.24 до 0.10
- `app/main.py` — FastAPI с lifespan-загрузкой модели + REST `/predict` + смонтированный Gradio на корневом пути `/`
- `models/wine_model.pkl` — сериализованный `DecisionTreeClassifier`. В git не хранится, собирается ноутбуком
- `tests/` — pytest-тесты на REST-эндпоинт и Gradio-роут
- `Dockerfile` + `.github/workflows/` — CI/CD, автодеплой на VPS через GHCR + SSH

## Архитектура

```mermaid
flowchart LR
    Browser[Browser] -->|GET /| Gradio[Gradio UI]
    Client[Programmatic client] -->|POST /predict| REST[FastAPI REST]
    Gradio -->|joblib.load| Model
    REST -->|joblib.load| Model
    Model[wine_model.pkl]
```

## Как запустить локально

```bash
conda create -n task-api python=3.11 -y
conda activate task-api
pip install -r requirements.txt

# 1) обучаем модель (получим models/wine_model.pkl)
jupyter nbconvert --to notebook --execute notebooks/wine_train_solution.ipynb --output wine_train_solution.ipynb

# 2) запускаем сервис
uvicorn app.main:app --reload
```

Откройте `http://127.0.0.1:8000/` для Gradio, `http://127.0.0.1:8000/docs` для Swagger.

## Скриншот

![Gradio-интерфейс](screenshots/test_public_url.jpg)

## Стек

Python 3.11 · FastAPI · Pydantic v2 · scikit-learn 1.6 · Gradio 5 · pytest · Docker · GitHub Actions · GHCR · nginx · Let's Encrypt
