from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

load_dotenv()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

from .database import engine
from .models import m_coins, m_users
from .routers import r_coins, r_users

m_users.Base.metadata.create_all(engine)
m_coins.Base.metadata.create_all(engine)

app.include_router(r_users.router)
app.include_router(r_coins.router)