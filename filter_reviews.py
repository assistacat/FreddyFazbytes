import pandas as pd
from pathlib import Path

data_path = Path("/Users/jiayi/Downloads/techjam/cleaned_reviews.csv")
df = pd.read_csv(data_path)

# Define what is "empty"
empty_values = ["No reviews"]

# Filter out rows where review is empty or in the above list
df_clean = df[~df["review"].isin(empty_values)].copy()

# Save as a new file
output_path = Path("/Users/jiayi/Downloads/techjam/cleaned_reviews_noempty.csv")
df_clean.to_csv(output_path, index=False)

print(f"Cleaned dataset saved to {output_path}")
