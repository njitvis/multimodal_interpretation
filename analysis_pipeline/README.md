# Analysis Pipeline

This repository contains scripts and data for running both quantitative and qualitative analyses of chart caption ratings and interpretability.

## 🚀 Getting Started

### Step-by-Step Instructions

#### 0. **Initial Data Setup**
Copy the following input files into the `analysis_pipeline/data` folder:

- `captions.csv`
- `chart_vectors_complete.csv`
- `claim_evidence_interpretation.csv`

#### 1. **Prepare Rater Ratings**
Copy the CSV file in `analysis_pipeline/data` containing the ratings of all raters, grouped as needed.

---

## 🔢 Quantitative Analysis

#### 2. **Compute Average Ratings**
Run the following script to compute average ratings:
```bash
python average_rating.py
```

#### 3. **Explore Data Distributions**
You can run any of the scripts in the `simple_analysis` folder to explore distributions and trends:
```bash
cd simple_analysis
python script_name.py
```
*(Scripts in this folder can be run in any order.)*

#### 4. **Visualize with Local Data Viewer**
To visualize keyword and L1–L4 distribution for interpretability:

- Run:
  ```bash
  python export_caption_feature.py
  ```
- Copy the generated `download.csv` from `analysis_pipeline/data` to:
  ```
  local-data-viewer/public/data
  ```

Then open the local-data-viewer UI in your browser to explore the data.

---

## 🧠 Qualitative Analysis

#### 5. **Prepare Reasons Data**
Copy `all_reasons.csv` to the `analysis_pipeline/data` folder.

#### 6. **Segment Reason Phrases**
Run the reason segmentation script:
```bash
python qualitative_analysis/reason_segmentation.py
```

#### 7. **Extract Segmented Reasons**
Extract the segmented reasons:
```bash
python qualitative_analysis/extract_reason_segmentation.py
```

#### 8. **Assign a label to each reason based on usefulness**
If the reason indicates certain information in caption helped them understand the visualization, it is marked as useful by llama3 model:
```bash
python qualitative_analysis/group_by_usefulness.py
```

#### 9. **Cluster reasons of differnt levels of usefulness**
login to HF first
```bash
python qualitative_analysis/code_usefulness_groups.py
```

#### 10. **Summarize clusters**
```bash
python qualitative_analysis/summarize_clusters.py
```