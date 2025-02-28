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
        "fal-ai/recraft-20b",
        arguments={
            "prompt": prompts['prompts'][i]['prompt'],
            "image_size": "square_hd",
            "style": "any",
            "colors": [],
        },
        with_logs=True,
        on_queue_update=on_queue_update,
    )
    print(result)
    
    image = requests.get(result['images'][0]['url'])
    with open(f"python/result/recraft-ai/recraft-20b/{str(i)}.png", "wb") as f:
        f.write(image.content)