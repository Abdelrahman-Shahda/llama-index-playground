from dotenv import load_dotenv

load_dotenv()

import logging
import os
import uvicorn
from app.api.routers.chat import chat_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.engine.index import initialize_bot
from app.embedchain.index import initialize_bot as embedchain_bot_intialize

app = FastAPI()

environment = os.getenv("ENVIRONMENT", "dev")  # Default to 'development' if not set



if environment == "dev":
    logger = logging.getLogger("uvicorn")
    logger.warning("Running in development mode - allowing CORS for all origins")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(chat_router, prefix="/api/chat")

@app.on_event("startup")
async def startup():
    mode=os.getenv("MODE", "llama-index")
    if mode == "llama-index":
        initialize_bot()
    else:
        embedchain_bot_intialize()

if __name__ == "__main__":
    uvicorn.run(app="main:app",port=8001, reload=True)
