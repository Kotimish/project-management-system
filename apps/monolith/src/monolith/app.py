from fastapi import FastAPI

from monolith.lifespan import lifespan
from monolith.auth.presentation.api import router as auth_router
from monolith.client.presentation.api import router as client_router
from monolith.user_profile.presentation.api import router as user_profile_router

app = FastAPI(lifespan=lifespan)
# Регистрация роутеров
app.include_router(auth_router)
app.include_router(client_router)
app.include_router(user_profile_router)


@app.get("/health/")
async def health_check():
    """
    Простая проверка работоспособности веб-приложения
    :return: Словарь с ключом "status": "ok", если сервер запушен.
    """
    return {"status": "ok"}
