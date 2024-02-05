import logging
import os
from llama_index import (
    StorageContext,
    load_index_from_storage,
)

from app.engine.constants import STORAGE_DIR
from app.engine.context import create_service_context
from llama_index.prompts import ChatPromptTemplate, PromptTemplate
from llama_index.llms import ChatMessage, MessageRole
import llama_index
from llama_index.prompts import 

llama_index.set_global_handler("simple")

index = None

def get_text_qa_prompt():
    chat_text_qa_msgs = [
        ChatMessage(
          role=MessageRole.SYSTEM,
          content=(
            "You are an expert digital verification engineer that is trusted around the world.\n"
            "Answer the following questions about PSS and provide a simple PSS code snippet only if it would be relevant using the provided context information, "
            "and your prior knowledge.\n"
            "Some rules to follow:\n"
            "1. Never directly reference the given context in your answer.\n"
            "2. Avoid using the exact pss example from the context \n"
            "3. Avoid statements like 'Based on the context, ...' or "
            "'The context information ...' or anything along "
            "those lines."

    ),
      ),
        ChatMessage(
            role=MessageRole.USER,
            content=(
                "Context information is below.\n"
                "---------------------\n"
                "{context_str}\n"
                "---------------------\n"
                "Given the context information and your prior knowledge, "
                "answer the question: {query_str}\n"
            ),
        ),
    ]
    text_qa_template = ChatPromptTemplate(chat_text_qa_msgs)
    return text_qa_template

def initialize_bot():
    global index
    service_context = create_service_context()
    # check if storage already exists
    if not os.path.exists(STORAGE_DIR):
        raise Exception(
            "StorageContext is empty - call 'python app/engine/generate.py' to generate the storage first"
        )
    logger = logging.getLogger("uvicorn")
    # load the existing index
    logger.info(f"Loading index from {STORAGE_DIR}...")
    storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
    index = load_index_from_storage(storage_context, service_context=service_context)
    logger.info(f"Finished loading index from {STORAGE_DIR}")


def get_response(chatHistory):
    global index
    # Text QA Prompt
    text_qa_template = get_text_qa_prompt()
    query_engine = index.as_query_engine(
        text_qa_template=text_qa_template,
        streaming=True
    )
    chat_engine = index.as_chat_engine()