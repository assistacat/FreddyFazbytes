import openai
import pandas as pd
from pathlib import Path

data_path = Path("/Users/jiayi/Downloads/techjam/cleaned_reviews.csv")
df = pd.read_csv(data_path)

with open("/Users/jiayi/Downloads/techjam/prompts/few_shot_prompt.txt", "r") as f:
    few_shot_prompt = f.read()

from gemma import GemmaClient
import pandas as pd
from pathlib import Path


API_KEY = "AIzaSyAA2hxaCtptJ5knSxQFfbWjBy43dEoV9cI"
MODEL_NAME = "gemma-2-9b-instruct"
PROMPT_TYPE = "few"

# Paths
DATA_PATH = Path("cleaned_reviews_nonempty.csv")
OUTPUT_PATH = Path("classified_reviews_gemma.csv")

client = GemmaClient(api_key=API_KEY)


df = pd.read_csv(DATA_PATH)

prompt_file = "prompts/few_shot_prompt.txt" if PROMPT_TYPE == "few" else "prompts/zero_shot_prompt.txt"
with open(prompt_file, "r") as f:
    base_prompt = f.read()

categories = []

for idx, row in df.iterrows():
    # Fill in placeholders
    prompt = base_prompt.format(
        clean_text=row["review"],
        rating=row["rating"],
        store_name=row["store_name"],
        reviewer_name=row["reviewer_name"]
    )

    response = client.generate(
        model=MODEL_NAME,
        prompt=prompt,
        temperature=0
    )

    category = response.text.strip()
    categories.append(category)

    print(f"{idx+1}/{len(df)} | Review: {row['review'][:50]}... | Predicted: {category}")

df["category"] = categories
df.to_csv(OUTPUT_PATH, index=False)
print(f"Classification complete! Saved to {OUTPUT_PATH}")