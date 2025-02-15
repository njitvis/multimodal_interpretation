#### add image background and format annotations
import os
import json
from PIL import Image
from utils import process_image, generate_annotation
from constants import CLASS_MAPPING

PARENT = '<PATH_TO_PROJECT>/train_yolo/datasets/'
PATH_BASE = f'{PARENT}output_dataset/'
FOLDERS = ['train', 'test', 'val']

for folder in FOLDERS:
  image_output = f"{PARENT}charts/images/" + folder
  label_output = f"{PARENT}charts/labels/" + folder
  if not os.path.exists(image_output):
      os.makedirs(image_output)
  if not os.path.exists(label_output):
      os.makedirs(label_output)

  input_dir = f"{PATH_BASE}images/{folder}"
  for file_name in os.listdir(input_dir):
    image_path = os.path.join(input_dir, file_name)
    
    chart = Image.open(image_path).convert("RGB")
    chart_width, chart_height = chart.size
    chart.close()
    
    modified_image, position, text_height = process_image(image_path)
    
    output_image_path = os.path.join(image_output, file_name)
    modified_image.convert("RGB").save(output_image_path)

    # Chart bounding box
    bbox_y1 = text_height if "top" in position else 0
    bbox_x1 = chart_width if "right" in position else 0
    chart_bbox = (bbox_x1, bbox_y1, bbox_x1 + chart_width, bbox_y1 + chart_height)
    file_name_base = file_name.split(".jpg")[0]
    with open(f'{PATH_BASE}/labels/{folder}/{file_name_base}.json', 'r') as file:
      data = json.load(file)
    cls = CLASS_MAPPING[data["task1"]["output"]["chart_type"]]
    annotation = generate_annotation(cls, chart_bbox, modified_image.size)
    annotation_path = os.path.join(label_output, file_name_base + ".txt")
    with open(annotation_path, "w") as f:
        f.write(annotation)
