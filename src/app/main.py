from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.svg_drawer import svg_drawer
from app.routes.text2audio import text_2_audio_router

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(text_2_audio_router)
app.include_router(svg_drawer)
# app.include_router(log_router)
