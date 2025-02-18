# Multimodal Interpretation

## Scripts

### `/chart_qna/single_view_qa.ipynb`
This notebook contains experiments related to generating questions and answers

#### 1. Generating 10 Questions With Only Chart, Answers, and Answers with Caption for Single View Charts
- This section runs code snippets that:
  - Generate 10 questions given a chart.
  - Provide answers to those 10 questions based on the question alone.
  - Provide answers again, this time with the caption as additional context.

#### 2. Generating 10 Questions With the Caption and Chart Both, Answers, and Answers with Caption for Single View Charts
- This section runs code snippets that:
  - Generate 10 questions given a chart and its corresponding caption.
  - Provide answers to those 10 questions based on the question alone.
  - Provide answers again, this time with the caption as additional context.

### `/chart_qna/sbert_cosine.ipynb`
This notebook calculates similarity between question and answers with different conditions

#### 1. Calculating Similarity Between Answers With and Without Caption
- This section runs code that:
  - Generates embeddings using SBERT 'all-MiniLM-L6-v2' model
  - Calculates cosine similarity between 'answers' and 'answers without caption'