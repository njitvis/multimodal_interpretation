from constants import CLASS_MAPPING

classes = list(CLASS_MAPPING.keys())
with open("../charts.yaml", "w") as f:
    f.write(f"""
    train: charts/images/train
    val: charts/images/val
    test: charts/images/test
    nc: {len(classes)}
    names: {classes}
    """)
