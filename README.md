# FreddyFazbytes

## Overview
FreddyFazbytes is a data analysis and machine learning project focused on the moderation and analysis of Google location reviews. The project aims to filter, clean, and analyze user-generated reviews to ensure only valid, relevant, and policy-compliant content is retained for further analysis. It includes data cleaning, exploratory data analysis (EDA), prompt engineering, and evaluation pipelines.

## Table of Contents
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Data Sources](#data-sources)
- [Notebooks](#notebooks)
- [Scripts](#scripts)
- [Results and Visualizations](#results-and-visualizations)
- [Contributing](#contributing)
- [License](#license)

## Project Structure
```
├── data/                # Datasets (raw, cleaned, evaluation splits)
├── notebooks/           # Jupyter notebooks for EDA, cleaning, pipelines
├── scripts/             # Python scripts for prompt testing and evaluation
├── src/                 # Source code for data processing
├── prompts/             # Prompt templates for classification
├── plots/               # Generated plots and visualizations
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
```

## Installation
1. Clone the repository:
	```
	git clone https://github.com/assistacat/FreddyFazbytes.git
	cd FreddyFazbytes
	```
2. (Optional) Create and activate a virtual environment:
	```
	python -m venv venv
	.\venv\Scripts\activate
	```
3. Install dependencies:
	```
	pip install -r requirements.txt
	```

## Usage
### Data Cleaning & EDA
Run the Jupyter notebooks in the `notebooks/` directory for data cleaning and exploratory data analysis:
```
jupyter notebook notebooks/data_cleaning.ipynb
jupyter notebook notebooks/exploratory_data_analysis.ipynb
```

### Running Scripts
Scripts for prompt testing and evaluation are in the `scripts/` directory. Example:
```
python scripts/test_prompts.py
```

### Evaluation Split
To create evaluation splits, use:
```
python src/make_eval_split.py
```

## Data Sources
- `data/cleaned_reviews_noempty.csv`: Main cleaned dataset for analysis
- `data/cleaned_reviews.csv`: Cleaned reviews (may include empty rows)
- `data/google_reviews_apify_dataset.csv`: Raw Google reviews
- `data/kaggle_reviews_raw.csv`: Raw reviews from Kaggle
- `data/fewshot_pool.csv`: Pool for few-shot prompt examples
- `data/labelled_subset.csv`: Manually labelled subset for evaluation
- `data/eval/balanced_eval.csv`: Balanced evaluation split

## Notebooks
- `notebooks/data_cleaning.ipynb`: Data cleaning and preprocessing
- `notebooks/exploratory_data_analysis.ipynb`: Exploratory data analysis and visualization
- `notebooks/Multi-task Pipeline.ipynb`: Multi-task learning pipeline
- `notebooks/Prototype Inference Pipeline.ipynb`: Prototype inference pipeline

## Scripts
- `scripts/test_prompts.py`: Test prompt templates and model responses
- `scripts/test_prompts_gemma_api.py`: Test prompts using the Gemma API
- `src/make_eval_split.py`: Script to create evaluation splits

## Results and Visualizations
Generated plots are saved in the `plots/` directory:
- `rating_distribution.png`: Distribution of review ratings
- `review_length_distribution.png`: Distribution of review lengths
- `review_length_vs_rating.png`: Boxplot of review length by rating
- `word_cloud.png`: Word cloud of most common words in reviews

## Prompts
Prompt templates for review classification are in the `prompts/` directory, including few-shot and zero-shot examples.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for improvements or bug fixes.

## License
This project is for educational and research purposes. Please see the repository for license details.