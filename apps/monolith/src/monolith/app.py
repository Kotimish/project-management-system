from fastapi import FastAPI

from monolith.auth.presentation.api import router as auth_router
from monolith.lifespan import lifespan

app = FastAPI(lifespan=lifespan)
# Регистрация роутеров
app.include_router(auth_router)


@app.get("/health/")
async def health_check():
    """
    Простая проверка работоспособности веб-приложения
    :return: Словарь с ключом "status": "ok", если сервер запушен.
    """
    return {"status": "ok"}
