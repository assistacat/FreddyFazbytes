import openai
import pandas as pd
from pathlib import Path

# Load your cleaned reviews file
data_path = Path("/Users/jiayi/Downloads/techjam/cleaned_reviews.csv")
df = pd.read_csv(data_path)

# Load the few-shot prompt
with open("/Users/jiayi/Downloads/techjam/prompts/few_shot_prompt.txt", "r") as f:
    few_shot_prompt = f.read()

categories = []

# Loop through all rows
for idx, row in df.iterrows():
    # Fill placeholders in the prompt
    prompt = few_shot_prompt.format(
        clean_text=row["review"],
        rating=row["rating"],
        store_name=row["store_name"],
        reviewer_name=row["reviewer_name"]
    )

    # Send prompt to GPT
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # use gpt-4o for better accuracy if needed
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    # Extract category
    category = response["choices"][0]["message"]["content"].strip()
    categories.append(category)

# Add results back into the DataFrame
df["category"] = categories

# Save into a new file
output_path = Path("/Users/jiayi/Downloads/techjam/classified_reviews.csv")
df.to_csv(output_path, index=False)

print(f"✅ Classification complete! Saved to {output_path}")
