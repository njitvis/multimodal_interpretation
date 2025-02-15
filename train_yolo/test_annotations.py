import cv2
import os

def draw_bounding_boxes(image_path, annotation_file):
    # Read the image
    image = cv2.imread(image_path)

    # Read YOLO-format annotation file
    with open(annotation_file, 'r') as file:
        lines = file.readlines()

    # Loop through each line in the annotation file
    for line in lines:
        # Parse the YOLO annotation line
        class_id, x_center, y_center, width, height = map(float, line.strip().split())
        
        # Get image dimensions
        image_height, image_width, _ = image.shape

        # Convert YOLO normalized values to pixel values
        x_center = int(x_center * image_width)
        y_center = int(y_center * image_height)
        bbox_width = int(width * image_width)
        bbox_height = int(height * image_height)

        # Calculate top-left corner and bottom-right corner of the bounding box
        x1 = x_center - bbox_width // 2
        y1 = y_center - bbox_height // 2
        x2 = x_center + bbox_width // 2
        y2 = y_center + bbox_height // 2

        color = (0, 0, 255)
        thickness = 5
        cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

    # Display the image with the bounding boxes
    cv2.imshow("Image with Bounding Boxes", image)
    cv2.waitKey(1000000)
    cv2.destroyAllWindows()

# Example usage
# image_path = "./datasets/charts/images/train/PMC1790633___g007.jpg"  # Replace with your image path
# annotation_file = "./datasets/charts/labels/train/PMC1790633___g007.txt"  # Replace with your annotation file path (YOLO format)
# draw_bounding_boxes(image_path, annotation_file)


for filename in os.listdir('./datasets/charts/images/val'):
    image_path = os.path.join('./datasets/charts/images/val', filename)
    annotation_file = os.path.join('./datasets/charts/labels/val', filename.split('.jpg')[0] + '.txt')
    draw_bounding_boxes(image_path, annotation_file)