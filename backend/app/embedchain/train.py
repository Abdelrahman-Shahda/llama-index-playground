import os
from embedchain import Pipeline as App

# Create a bot instance
bot = App.from_config(yaml_path="./app/embedchain/config.yaml")

bot.reset()
# Embed online resources
bot.add("https://llms-te.s3.eu-north-1.amazonaws.com/pss_LRM.pdf", metadata={"source_type": "LRM"})
bot.add("https://llms-te.s3.eu-north-1.amazonaws.com/grammer.txt", metadata={"source_type": "grammer"})