import os
from dotenv import load_dotenv
import fal_client
import json
import requests

# Load the environment variables
load_dotenv()
os.environ["FAL_KEY"] = os.environ.get("FAL_CLIENT_ID")

# Define the on_queue_update function
def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
           print(log["message"])

prompts = json.load(open("python/prompt.json"))

for i in range(len(prompts['prompts'])):
    result = fal_client.subscribe(
        "fal-ai/ideogram/v2a",
        arguments={
            "prompt": prompts['prompts'][i]['prompt'],
            "aspect_ratio": "1:1",
            "expand_prompt": True,
            "seed": 42,
            "style": "auto",
            "negative_prompt": "",
        },
        with_logs=True,
        on_queue_update=on_queue_update,
    )
    
    image = requests.get(result['images'][0]['url'])
    with open(f"python/result/ideogram-ai/v2a/{str(i)}.png", "wb") as f:
        f.write(image.content)