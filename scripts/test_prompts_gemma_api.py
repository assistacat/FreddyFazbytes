import requests
import pandas as pd
from pathlib import Path
import time

API_KEY = "AIzaSyAA2hxaCtptJ5knSxQFfbWjBy43dEoV9cI"
MODEL = "gemma-2-9b-instruct"
PROMPT_TYPE = "few"

DATA_PATH = Path("cleaned_reviews_noempty.csv")
OUTPUT_PATH = Path("classified_reviews_gemma.csv")


prompt_file = Path("prompts/few_shot_prompt.txt") if PROMPT_TYPE == "few" else Path("prompts/zero_shot_prompt.txt")
with open(prompt_file, "r") as f:
    base_prompt = f.read()


df = pd.read_csv(DATA_PATH)
categories = []


def call_gemma(prompt):
    url = "https://api.gemma.ai/v1/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "prompt": prompt,
        "temperature": 0
    }
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    return response_json["choices"][0]["text"].strip()  


for idx, row in df.iterrows():
    prompt = base_prompt.format(
        clean_text=row["review"],
        rating=row["rating"],
        store_name=row["store_name"],
        reviewer_name=row["reviewer_name"]
    )
    
    try:
        category = call_gemma(prompt)
    except Exception as e:
        print(f"Error on row {idx}: {e}")
        category = "ERROR"

    categories.append(category)
    print(f"{idx+1}/{len(df)} | Predicted: {category}")
    time.sleep(1)


df["category"] = categories
df.to_csv(OUTPUT_PATH, index=False)
print(f"Classification complete! Saved to {OUTPUT_PATH}")
