from PIL import Image, ImageDraw, ImageFont
import os
import random
import xml.etree.ElementTree as ET
from lorem_text import lorem





def create_text_overlay(image, columns=1, position="top", font_size = 12):
    """Overlay text on the chart image."""
    font = ImageFont.load_default()  # Replace with a TTF font for better visuals if available

    # Determine text area size
    image_width, image_height = image.size
    text_width = image_width / columns

    # Generate dummy text for the overlay
    lorem_text = lorem.words(random.randint(50, 100))
    
    text = [""]
    for word in lorem_text.split(" "):
        new_line = text.pop()
        new_line_len = font.getbbox(f"{new_line} {word}")[2]
        
        if new_line_len >= text_width:
            text.append(f"{new_line}\n")
            text.append(word)
        else:
            text.append(f"{new_line} {word}")

    text_height = font_size * len(text)
    # Create overlay
    overlay = Image.new("RGBA", (image_width, image_height if "side" in position else text_height), (255, 255, 255, 255))
    overlay_draw = ImageDraw.Draw(overlay)
    for i, line in enumerate(text):
        overlay_draw.text(xy=(0, i * font_size), 
                          text=line,
                          fill="black", font=font)
        if columns == 2:
            overlay_draw.text(xy=(text_width, i * font_size), 
                          text=line,
                          fill="black", font=font)
            
    # Place overlay on top or bottom of the image
    if position == "top":
        combined = Image.new("RGBA", (image_width, image_height + text_height))
        combined.paste(overlay, (0, 0))
        combined.paste(image, (0, text_height))
    elif position == "bottom":
        combined = Image.new("RGBA", (image_width, image_height + text_height))
        combined.paste(image, (0, 0))
        combined.paste(overlay, (0, image_height))
    elif position == "left_side":
            combined = Image.new("RGBA", (image_width * 2, image_height))
            combined.paste(image, (0, 0))
            combined.paste(overlay, (image_width, 0))
    elif position == "right_side":
        combined = Image.new("RGBA", (image_width * 2, image_height))
        combined.paste(image, (image_width, 0))
        combined.paste(overlay, (0, 0))
    else:
        raise ValueError("Invalid position. Use 'top' or 'bottom'.")

    return combined, text_height





def generate_annotation(cls, chart_bbox, image_size):
    """Generate YOLO annotation."""
    class_id = cls  # Assuming charts are class 0
    image_width, image_height = image_size

    # Calculate YOLO format bounding box
    x_center = (chart_bbox[0] + chart_bbox[2]) / 2.0
    y_center = (chart_bbox[1] + chart_bbox[3]) / 2.0
    width = chart_bbox[2] - chart_bbox[0]
    height = chart_bbox[3] - chart_bbox[1]

    x_center_norm = x_center / image_width
    y_center_norm = y_center / image_height
    width_norm = width / image_width
    height_norm = height / image_height

    yolo_annotation = f"{class_id} {x_center_norm} {y_center_norm} {width_norm} {height_norm}"

    return yolo_annotation





      
def process_image(image_path):
    """Process chart images to create variations and annotations."""
    image = Image.open(image_path).convert("RGB")

    scenarios = [
        (1, "top"), (1, "bottom"), (1, "top_and_bottom"),
        (2, "top_and_bottom"), (2, "top"), (2, "bottom"),
        (1, "left_side"), (1, "right_side")
    ]

    idx = random.randint(0, 7)
    (columns, position) = scenarios[idx]
    modified_image = image.copy()
    font_size = 12

    if position == "top_and_bottom":
        modified_image, text_height = create_text_overlay(modified_image, columns, "top", font_size)
        modified_image, _ = create_text_overlay(modified_image, columns, "bottom", font_size)
    else:
        modified_image, text_height = create_text_overlay(modified_image, columns, position, font_size)

    return modified_image, position, text_height
