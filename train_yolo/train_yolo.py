from ultralytics import YOLO

def main():
    model = YOLO("./runs/detect/train4/weights/best.pt")

    model.train(
        data="<PATH_TO_PROJECT>/train_yolo/charts.yaml",
        epochs=50,
        batch=16,
        imgsz=640,
        device="cuda",
        workers=8,
        amp=False
    )

if __name__ == "__main__":
    main()
