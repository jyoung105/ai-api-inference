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
        "fal-ai/imagen3/fast",
        arguments={
            "prompt": prompts['prompts'][i]['prompt'],
            "negative_prompt": "",
            "aspect_ratio": "1:1",
            "num_images": 1,
            "seed": 42,
        },
        with_logs=True,
        on_queue_update=on_queue_update,
    )
    
    image = requests.get(result['images'][0]['url'])
    with open(f"python/result/google/imagen-3-fast/{str(i)}.png", "wb") as f:
        f.write(image.content)