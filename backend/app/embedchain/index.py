import os
from embedchain import Pipeline as App
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

embedchain_bot = None
def get_response_with_rag(question):
    global embedchain_bot
    app = embedchain_bot
    response = app.query(question)
    return response

def initialize_bot():
    global embedchain_bot
    embedchain_bot = App.from_config(yaml_path="./app/embedchain/config.yaml")

def get_engine():
    global embedchain_bot
    return embedchain_bot
