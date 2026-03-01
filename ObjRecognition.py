from ultralytics import YOLO
from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction
import location
import GettingClimate
import torch
import GettingFile
import AiResponce

IMG_PATH = GettingFile.Save_Root()
MODEL_PATH = 'yolov8x-oiv7.pt'
CONF_THRESHOLD = 0.25
IOU_THRESHOLD  = 0.45
IMG_SIZE       = 1280




TARGET_CLASSES = {
    'Tree', 'Plant', 'Person', 'Car', 'Truck',
    'Bus', 'Motorcycle', 'Vehicle', 'Flowerpot', 'Houseplant'
}


print("\n========== YOLO INFERENCE ==========")
model = YOLO(MODEL_PATH)

results = model(
    IMG_PATH,
    conf=CONF_THRESHOLD,
    iou=IOU_THRESHOLD,
    imgsz=IMG_SIZE,
    augment=True,
    agnostic_nms=True,
    verbose=False
)

counts = {name: 0 for name in TARGET_CLASSES}

for box in results[0].boxes:
    cls_id = int(box.cls.item())
    conf   = float(box.conf.item())
    name   = model.names[cls_id]

    if name in TARGET_CLASSES:
        counts[name] += 1
        print(f"  Detected: {name:<15} conf={conf:.2f}")

print("\n--- Standard YOLO Counts ---")
for cls, count in sorted(counts.items()):
    if count > 0:
        print(f"  {cls:<15}: {count}")

results[0].show()


print("\n========== SAHI SLICED INFERENCE ==========")

sahi_model = AutoDetectionModel.from_pretrained(
    model_type='yolov8',
    model_path=MODEL_PATH,
    confidence_threshold=CONF_THRESHOLD,
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
)

sahi_result = get_sliced_prediction(
    IMG_PATH,
    sahi_model,
    slice_height=640,
    slice_width=640,
    overlap_height_ratio=0.2,
    overlap_width_ratio=0.2,
)

sahi_counts = {name: 0 for name in TARGET_CLASSES}

for obj in sahi_result.object_prediction_list:
    name = obj.category.name
    conf = obj.score.value

    if name in TARGET_CLASSES:
        sahi_counts[name] += 1
        print(f"  Detected: {name:<15} conf={conf:.2f}")

print("\n--- SAHI Sliced Counts ---")
for cls, count in sorted(sahi_counts.items()):
    if count > 0:
        print(f"  {cls:<15}: {count}")


sahi_result.export_visuals(export_dir="sahi_output/")
print("\nSAHI visual saved to: sahi_output/")


print("\n========== MERGED COUNTS (SAHI wins on small objects) ==========")
merged_counts = {}
for cls in TARGET_CLASSES:
    merged_counts[cls] = max(counts[cls], sahi_counts[cls])

for cls, count in sorted(merged_counts.items()):
    if count > 0:
        print(f"  {cls:<15}: {count}")


print("\n========== LOCATION & CLIMATE ==========")

geo_info = location.get_ip_geolocation()
print(f"Geolocation: {geo_info}")

longitude = location.get_longitute()
latitude  = location.get_latitute()
print(f"Coordinates: lat={latitude}, lon={longitude}")

Climate = GettingClimate.get_climate_data(longitude, latitude)


def Green_Index():
    green_objects = (
        merged_counts.get('Tree', 0) +
        merged_counts.get('Plant', 0) +
        merged_counts.get('Houseplant', 0) +
        merged_counts.get('Flowerpot', 0)
    )

    total_objects = sum(merged_counts.values())

    if total_objects == 0:
        return 0

    return round(green_objects / total_objects,2)

def TrafficIndex():
    traffic_objects = (
        merged_counts.get('Car', 0) +
        merged_counts.get('Truck', 0) +
        merged_counts.get('Bus', 0) +
        merged_counts.get('Motorcycle', 0) +
        merged_counts.get('Vehicle', 0)
    )

    total_objects = sum(merged_counts.values())

    if total_objects == 0:
        return 0
    else:
        return round(traffic_objects / total_objects,2)

def HumanDensityIndex():
    human_objects = merged_counts.get('Person', 0)

    total_objects = sum(merged_counts.values())
    if total_objects == 0:
        return 0
    else:
        return round(human_objects / total_objects,2)


def FinalRep():
    print("\n========== FINAL REPORT ==========")
    print(f"Image         : {IMG_PATH}")
    print(f"Model         : {MODEL_PATH}")
    print(f"Location      : {geo_info}")
    print(f"Coordinates   : lat={latitude}, lon={longitude}")
    print(f"Green Coverage Index: {Green_Index()}")
    print(f"Traffic Density Index: {TrafficIndex()}")
    print(f"Human Activity Index: {HumanDensityIndex()}")
    print(f"Climate: {Climate}")
    print(f"\nDetected Objects (merged):")
    for cls, count in sorted(merged_counts.items()):
        if count > 0:
            print(f"  {cls:<15}: {count}")


FinalRep()
AiResponce.GetPromptAndResponse()
