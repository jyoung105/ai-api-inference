import requests
import json
from dotenv import load_dotenv
import os

# Load the environment variables
load_dotenv()
url = "https://api.minimaxi.chat/v1/image_generation"
HAILUO_AI_ID = os.environ.get("HAILUO_AI_ID")

# Load prompts from prompt.json
with open("python/prompt.json", "r") as f:
    prompts = json.load(f)

# Iterate through the prompts and generate images
for i, prompt_data in enumerate(prompts['prompts']):
    prompt = prompt_data['prompt']

    payload = json.dumps({
      "model": "image-01", 
      "prompt": prompt,
      "aspect_ratio": "1:1",
      "response_format": "url",
      "n": 1,
      "prompt_optimizer": True
    })
    headers = {
      'Authorization': f'Bearer {HAILUO_AI_ID}',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # Print the response
    print(response.json())

    # Save the image to the result folder
    result = response.json()
    if 'data' in result and len(result['data']) > 0 and 'url' in result['data'][0]:
        # Create the result directory if it doesn't exist
        os.makedirs("python/result/hailuo-ai", exist_ok=True)
        
        # Get the image from the URL
        image_url = result['data']['image_urls'][0]
        image = requests.get(image_url)
        
        # Save the image to a file with a numbered filename
        with open(f"python/result/hailuo-ai/{i}.png", "wb") as f:
            f.write(image.content)
        
        print(f"Image saved to python/result/hailuo-ai/{i}.png")
    else:
        print("No image URL found in the response")