# Chart Detection with YOLOv8n

This repository contains scripts and configurations to train a YOLOv8n model to detect charts in research papers. The dataset used for training requires restructuring and formatting before being used for training.

## Installation

1. Clone the repository:
   ```sh
   git clonehttps://github.com/njitvis/multimodal_interpretation.git
   cd multimodal_interpretation/train_yolo
   ```

2. Create a virtual environment:
   ```sh
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```

4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Download Dataset

Download the dataset from the provided URL:
```sh
wget https://www.dropbox.com/scl/fi/vy7gyemald8z6rohx9mxx/CHARTINFO_2024_Train.zip?rlkey=ki3q4bb02rzdpdbih17we63gm&dl=0 -O dataset1.zip
wget https://www.dropbox.com/scl/fi/am33424ochxs4yryprl0p/CHARTINFO_2024_Test.zip?rlkey=lcacxvgljcr5p3zo8t1uss63m&dl=0 -O dataset2.zip
unzip dataset1.zip -d <project_path>/multimodal_interpretation/train_yolo/datasets/input_charts
unzip dataset2.zip -d <project_path>/multimodal_interpretation/train_yolo/datasets/input_charts
```

## Preprocessing Steps

### 1. Structure the dataset folder
Run the `structure_folder.py` script to reorganize the dataset into the expected structure:
```sh
python structure_folder.py
```

### 2. Format dataset
The `format_data.py` script adds texts around the chart image to enhance detection:
```sh
python format_data.py
```

### 3. Generate YAML Configuration
Create the `charts.yaml` configuration file required by YOLOv8:
```sh
python dataset_yaml.py
```

## Train and Test the Model

### Train the Model
Run the training script:
```sh
python train_model.py
```

### Test the Model
Run the testing script:
```sh
python test_model.py
```

## Validate Annotations
To ensure the annotations in your dataset are correct, run:
```sh
python test_annotations.py
```

## Upload Model to Hugging Face
To upload the trained model to Hugging Face, update the authentication token in `backup_to_HF.py`, then run:
```sh
python backup_to_HF.py
```

## Contributing
Feel free to open issues and pull requests to improve the repository.

