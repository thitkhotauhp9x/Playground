from fastapi import FastAPI
# from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.routes.text2audio import text_2_audio_router
from app.routes.image_generation import image_generation_router


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # Cho phép các origin trong danh sách
    allow_credentials=True,
    allow_methods=["*"],                # Cho phép tất cả các phương thức (GET, POST, PUT, DELETE...)
    allow_headers=["*"],                # Cho phép tất cả các headers
)


app.include_router(text_2_audio_router)
app.include_router(image_generation_router)
