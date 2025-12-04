from fastapi import FastAPI
from monolith.presentation.api import health_router

app = FastAPI()
# Регистрация роутеров
app.include_router(health_router)
