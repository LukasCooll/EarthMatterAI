from ultralytics import YOLO
from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction
import location
import GettingClimate
import torch
import AiResponce
import os
import base64
import cv2

MODEL_PATH = 'yolov8x-oiv7.pt'
CONF_THRESHOLD = 0.25
IOU_THRESHOLD  = 0.45
IMG_SIZE       = 1280

TARGET_CLASSES = {
    'Tree', 'Plant', 'Person',
    'Car', 'Truck', 'Bus', 'Motorcycle',
    'Flowerpot', 'Houseplant'
}



def get_annotated_image_base64(results):
    annotated_array = results[0].plot()
    _, buffer = cv2.imencode('.jpg', annotated_array)
    b64_string = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{b64_string}"


def run_detection(img_path, living_type="Indoor"):
    """
    Runs YOLO + SAHI detection, calculates indices, generates AI report and visualizations.
    img_path: path to image
    living_type: "Indoor" or "Outdoor" (from HTML form)
    """

    # ===== YOLO INFERENCE =====
    model = YOLO(MODEL_PATH)
    results = model(
        img_path,
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

    sahi_model = AutoDetectionModel.from_pretrained(
        model_type='yolov8',
        model_path=MODEL_PATH,
        confidence_threshold=CONF_THRESHOLD,
        device='cuda:0' if torch.cuda.is_available() else 'cpu'
    )

    sahi_result = get_sliced_prediction(
        img_path,
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

    sahi_output_dir = "sahi_output"
    os.makedirs(sahi_output_dir, exist_ok=True)
    sahi_result.export_visuals(export_dir=sahi_output_dir)

    merged_counts = {cls: max(counts[cls], sahi_counts[cls]) for cls in TARGET_CLASSES}

    geo_info = location.get_ip_geolocation()
    longitude = location.get_longitute()
    latitude  = location.get_latitute()
    climate = GettingClimate.get_climate_data(longitude, latitude)

    def calculate_indexes(merged_counts):
        total_objects = sum(merged_counts.values())
        green_objects = (
                merged_counts.get('Tree', 0) +
                merged_counts.get('Plant', 0) +
                merged_counts.get('Houseplant', 0) +
                merged_counts.get('Flowerpot', 0)
        )
        traffic_objects = (
                merged_counts.get('Car', 0) +
                merged_counts.get('Truck', 0) +
                merged_counts.get('Bus', 0) +
                merged_counts.get('Motorcycle', 0) +
                merged_counts.get('Vehicle', 0)
        )
        human_objects = merged_counts.get('Person', 0)

        green_index = round(green_objects / total_objects, 2) if total_objects else 0
        traffic_index = round(traffic_objects / total_objects, 2) if total_objects else 0
        human_index = round(human_objects / total_objects, 2) if total_objects else 0

        return green_index, traffic_index, human_index

    green_index, traffic_index, human_index = calculate_indexes(merged_counts)

    response = AiResponce.GetPromptAndResponse(
        green_idx=green_index,
        traffic_idx=traffic_index,
        human_idx=human_index,
        climate=climate,
        living_type=living_type
    )

    print("\n========== FINAL REPORT ==========")
    print(f"Image: {img_path}")
    print(f"Location: {geo_info}")
    print(f"Coordinates: lat={latitude}, lon={longitude}")
    print(f"Green Index: {green_index}")
    print(f"Traffic Index: {traffic_index}")
    print(f"Human Index: {human_index}")
    print(f"Climate: {climate}")
    print(f"Living type: {living_type}")
    print("Merged Object Counts:")
    for cls, count in sorted(merged_counts.items()):
        if count > 0:
            print(f"  {cls:<15}: {count}")
    print("\nAI Response:")
    print(response)

    return {
        "merged_counts": merged_counts,
        "green_index": green_index,
        "traffic_index": traffic_index,
        "human_index": human_index,
        "geo_info": geo_info,
        "coordinates": (latitude, longitude),
        "climate": climate,
        "living_type": living_type,
        "ai_response": response,
        "image_path": img_path,
        "results": results,
    }