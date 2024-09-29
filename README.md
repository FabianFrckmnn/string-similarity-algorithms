# Data Matching and String Similarity Pipeline

This project is a data processing and matching pipeline designed to handle multiple CSV files, perform data preprocessing, and execute various matching algorithms to find similarities between records. The project utilizes machine learning and string-matching algorithms to compare and match records.

## Table of Contents

- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Setup and Installation](#setup-and-installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Algorithms](#algorithms)
- [Jupyter Notebooks](#jupyter-notebooks)
- [Testing](#testing)
- [License](#license)

## Project Structure

```
config/                 # Configuration files and utilities
data/                   # Input data and profiling results
figures/                # Figures and confusion matrices
models/                 # Pretrained models and outputs
notebooks/              # Jupyter Notebooks for testing and evaluation
scripts/                # Main scripts and algorithm implementations
tests/                  # Unit and integration tests
utils/                  # Utility functions and classes
main.py                 # Main script for running the pipeline
requirements.txt        # Python dependencies
environment.yml         # Conda environment configuration
.env.example            # Example environment configuration file
```

## Requirements

### Using `pip`

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Using `conda`

Create and activate the environment using the `environment.yml` file:

```bash
conda env create -f environment.yml
conda activate your-environment-name
```

Replace `your-environment-name` with the name of the environment specified in the `environment.yml` file.

## Setup and Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/FabianFrckmnn/string-similarity-algorithms.git
   cd string-similarity-algorithms
   ```

2. **Set up the environment:**
   - Use `pip` with `requirements.txt`, or
   - Use `conda` with `environment.yml`.

3. **Setup environment variables:**

   Copy the `.env.example` to `.env` and update the variables:

   ```bash
   cp .env.example .env
   ```

## Usage

To run the main data matching pipeline, execute:

```bash
python main.py
```

### Matching Algorithms

The following algorithms are supported and are implemented in the `scripts/algorithms/` directory:

- Levenshtein
- Dice Coefficient
- Jaccard Similarity
- N-gram Similarity
- Regex Matching
- TF-IDF Cosine Similarity

### Evaluation

To evaluate results, use the `evaluation.py` script, which computes metrics like accuracy, precision, recall, F1-score, and ROC-AUC.

## Jupyter Notebooks

The `notebooks/` directory contains Jupyter Notebooks demonstrating individual algorithms and evaluating their performance.

- `notebooks/algorithms/` contains algorithm-specific notebooks.
- `evaluate.ipynb` provides a consolidated view of the evaluation results across algorithms.

## Testing

The `tests/` directory contains unit tests for the project. To run the tests:

```bash
python tests/algotest.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
