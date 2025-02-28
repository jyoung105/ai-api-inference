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
        "fal-ai/flux-pro/v1.1",
        arguments={
            "prompt": prompts['prompts'][i]['prompt'],
            "image_size": "square_hd",
            "seed": 42,
            "num_images": 1,
            "enable_safety_checker": False,
            "safety_tolerance": 6,
            "output_format": 'png',
        },
        with_logs=True,
        on_queue_update=on_queue_update,
    )
    
    image = requests.get(result['images'][0]['url'])
    with open(f"python/result/black-forest-labs/flux-pro-v11/{str(i)}.png", "wb") as f:
        f.write(image.content)