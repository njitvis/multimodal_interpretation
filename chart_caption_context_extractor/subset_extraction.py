"""# Find Source"""

from sklearn.preprocessing import LabelEncoder
from ultralytics import YOLO
import pandas as pd
import fitz
import glob
import io
import os
from PIL import Image


l1_l4_clustered = pd.read_csv("./datasets/chart_vectors_complete.csv")
l1_l4_clustered = l1_l4_clustered[['image_id']]
l1_l4_clustered

captions = pd.read_csv("./datasets/chart_metadata.csv")
captions = captions[["image_id", "caption", "source"]]
captions

annotated_subset_source = pd.merge(l1_l4_clustered, captions, how='left', on='image_id')

files = annotated_subset_source.loc[:, "source"].unique()
pd.DataFrame(files).to_json('./datasets/pdf_sources.json', index=False)

"""# Extract Files"""


model = YOLO('./models/chart_detection.pt')

def find_chart(image_path):
    results = model.predict(image_path, conf=0.3)
    for result in results:
        boxes = []
        for box in result.boxes:
            for b in box.xyxy.tolist():
                if b[2] - b[0] > 100 and b[3] - b[1] > 100:
                  boxes.append({
                      "bbox": b,
                      "cls": int(box.cls)
                  })

    return boxes

# def tune_upper_bound(block_rect, y1):
#     if block_rect[1] < y1 and y1 < block_rect[3]:
#         y1 = block_rect[3]
#     return y1

os.makedirs('./extracted_charts', exist_ok=True)

try:
  found_captions = pd.read_csv('./datasets/found_captions.csv')
except:
  found_captions = pd.DataFrame(columns=["image_id", "source", "pageNumber", "caption", "type"])

# file =  "WGII_TAR_full_report-2.pdf"
for file in files:
    i = len(found_captions) + 1
    try:
        pdf_file = fitz.open(f'./datasets/PDFs/{file}')
    except:
       print(f'{file} not found.')
       continue
    for page_index in range(len(pdf_file)):
        page = pdf_file.load_page(page_index)

        pix = page.get_pixmap(dpi=300)
        image_bytes = pix.tobytes("png")
        page_image = Image.open(io.BytesIO(image_bytes))
        temp_image_path = f"temp_page_{page_index}.png"
        page_image.save(temp_image_path)
        bboxes = find_chart(temp_image_path)

        save = False
        for box in bboxes:
            x1, y1, x2, y2 = box["bbox"]
            # y2_old = y2
            # x1_old = x1
            # y1_old = y1

            text = page.get_text("dict")
            for block in text["blocks"]:
                span_rect = fitz.Rect(*block["bbox"])
                pdf_width, pdf_height = page.rect.width, page.rect.height
                img_width, img_height = pix.width, pix.height
                x_scale = img_width / pdf_width
                y_scale = img_height / pdf_height
                scaled_rect = [
                    span_rect.x0 * x_scale,
                    span_rect.y0 * y_scale,
                    span_rect.x1 * x_scale,
                    span_rect.y1 * y_scale,
                ]

#           # if x1 <= scaled_rect[0] and x2 >= scaled_rect[2]:
#           #     y1 = tune_upper_bound(scaled_rect, y1)

                block_text = ""
                for line in block.get("lines", []):
                    for span in line["spans"]:
                        block_text = block_text + span["text"]
                if block_text.lower().startswith("fig") and span_rect.intersects(fitz.Rect(box["bbox"])):
                    save = True
                    i += 1
                    found_captions.loc[len(found_captions)] = [i, pdf_file, page_index, block_text, box["cls"]]
                    # x1 = scaled_rect[0] - 50
                    # y2 = scaled_rect[1]

        if save:
            # try:
            cropped_image = page_image.crop((x1, y1, x2, y2))
            # except:
            #     cropped_image = page_image.crop((x1_old, y1_old, x2, y2_old))

            if cropped_image:
                try:
                    cropped_image.save(f'./extracted_charts/{i}.jpg')
                except:
                    print([i, pdf_file, page_index, block_text, box["cls"]], "not saved")


        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)

        found_captions.to_csv('./datasets/found_captions.csv', index=False)
        print(file, "scanned")

