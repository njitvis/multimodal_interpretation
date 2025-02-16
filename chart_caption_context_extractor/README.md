# Chart, Caption and Context Extraction from PDFs

## Overview
This project extracts charts, their captions, and contexts from PDF documents. The script processes PDFs stored in a specific directory, saves extracted captions in CSV format, and utilizes a YOLO model for chart extraction. Additionally, filtering and context extraction scripts are used to refine the extracted captions and provide contextual information.

## Project Structure
```
project/
│── datasets/
│   │── PDFs/                # Store all PDF files here
│── extracted_data.csv    # CSV files will be saved here
│── models/                   # Store the model used for chart extraction
│── subset_extraction.py     # Main script for chart extraction
│── subset_filtering.py      # Script to filter extracted captions
│── context_extraction.py    # Script to extract contextual sentences
│── README.md                 # This file
```

## Prerequisites
- Python 3.12+
- Virtual environment (venv)

## Installation

### 1. Create a Virtual Environment
Run the following command in the project root directory:
```sh
python -m venv venv
```

### 2. Activate Virtual Environment
- **Windows:**
  ```sh
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```sh
  source venv/bin/activate
  ```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

## Usage

### 1. Ensure Required Files Are in Place
- Place PDF files inside `chart_caption_context_extractor/datasets/PDFs`
- Ensure all CSV files are inside `chart_caption_context_extractor/datasets`
- Store the trained model in `chart_caption_context_extractor/models`

### 2. Run the Extraction Script
```sh
python subset_extraction.py
```

### 3. Run the Filtering Script
```sh
python subset_filtering.py
```

### 4. Run the Context Extraction Script
```sh
python context_extraction.py
```

### 5. Output
- Extracted charts will be saved in `chart_caption_context_extractor/extracted_charts`
- Extracted captions will be saved in `chart_caption_context_extractor/datasets/found_captions.csv`
- Filterd captions will be saved in `chart_caption_context_extractor/datasets/found_captions_with_vector.csv`
- Extracted contexts will be saved in `chart_caption_context_extractor/datasets/found_captions_with_context.csv`

## Notes
- If you encounter any issues, ensure dependencies are correctly installed.
- Modify `subset_extraction.py` to adjust extraction settings as needed.
- Modify `subset_filtering.py` to fine-tune the filtering criteria for captions.
- Modify `context_extraction.py` to adjust how contextual sentences are extracted.

