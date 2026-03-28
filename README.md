# EarthMatterAI

EarthMatterAI is a Flask-based web application that analyzes images to assess environmental sustainability metrics. It utilizes YOLO object detection combined with SAHI (Sliced Aided Hyper Inference) to identify environmental objects such as trees, plants, vehicles, and people, generating AI-driven insights about green spaces, traffic presence, and human activity.

## Features

- **Advanced Object Detection**: Combines YOLOv8 and SAHI for accurate multi-scale object detection.
- **Environmental Metrics**: Calculates three key indices:
  - **Green Index**: Percentage of vegetation (trees, plants, houseplants).
  - **Traffic Index**: Percentage of vehicles detected.
  - **Human Index**: Percentage of people detected.
- **Geolocation & Climate Integration**: Incorporates location data and climate information for context-aware analysis.
- **AI-Powered Insights**: Generates detailed analysis reports using AI based on environmental metrics.
- **Visual Feedback**: Provides annotated images showing detected objects.
- **Flexible Analysis**: Supports both indoor and outdoor environment classifications.

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Object Detection**: 
  - YOLOv8 (ultralytics)
  - SAHI (Sliced Aided Hyper Inference)
- **AI Analysis**: OpenAI API
- **Image Processing**: OpenCV
- **Frontend**: Vanilla HTML/JavaScript

## Project Structure

    EarthMatterAI/
    ├── main.py                 # Flask application entry point
    ├── ObjRecognition.py      # Core detection and analysis logic
    ├── AiResponce.py          # AI response generation
    ├── location.py            # Geolocation utilities
    ├── GettingClimate.py      # Climate data retrieval
    ├── imagecreation.py       # Image editing with AI
    ├── templates/
    │   └── index.html         # Web interface
    ├── uploads/               # User-uploaded images (created at runtime)
    ├── results/               # Detection results (created at runtime)
    └── sahi_output/           # SAHI visualization outputs (created at runtime)

## Installation

### Prerequisites

- Python 3.8+
- CUDA-compatible GPU (recommended for faster inference)
- OpenAI API key
- Valid location/climate data API credentials

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/thatoneluckyguy/EarthMatterAI.git
   cd EarthMatterAI
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install flask ultralytics sahi opencv-python openai torch torchvision
   ```

4. **Configure environment variables**:
   ```bash
   export IMAGEAPI_KEY="your-openai-api-key"
   export CLIMATE_API_KEY="your-climate-api-key"  # If applicable
   ```

5. **Download YOLOv8 model**:
   The application expects `yolov8x-oiv7.pt` in the project root. Download it from [Ultralytics YOLOv8 releases](https://github.com/ultralytics/ultralytics/releases).

## Usage

### Run the Application

   ```bash
   python main.py
   ```

The application will start on `http://0.0.0.0:5000`.

### Web Interface

1. Open your browser and navigate to `http://localhost:5000`.
2. Upload an image (JPG, PNG, etc.).
3. Select whether the image is from an "Indoor" or "Outdoor" settlement.
4. Click "Analyze".
5. View results:
   - AI-generated analysis report.
   - Green, Traffic, and Human indices.
   - Annotated image with detected objects.

### API Endpoint

**POST** `/upload`
- **Parameters**: 
  - `image` (file): Image to analyze.
  - `living_type` (string): "Indoor" or "Outdoor".
- **Response**:
  ```json
  {
    "image_path": "uploads/filename.jpg",
    "annotated_image_path": "results/filename.jpg",
    "annotated_image": "data:image/jpeg;base64,...",
    "result": {
      "ai_response": "Analysis text..."
    },
    "green_index": 0.25,
    "traffic_index": 0.15,
    "human_index": 0.10
  }
  ```

## Core Components

### ObjRecognition.py

Handles the complete detection pipeline:
- Runs YOLO inference on uploaded images.
- Applies SAHI for enhanced detection on cropped image regions.
- Merges detection results from both models.
- Calculates environmental indices.
- Integrates geolocation and climate data.
- Requests AI analysis.

**Detected Classes**:
Tree, Plant, Person, Car, Truck, Bus, Motorcycle, Vehicle, Flowerpot, Houseplant.

**Configuration**:
- `CONF_THRESHOLD`: 0.25 (confidence threshold).
- `IOU_THRESHOLD`: 0.45 (intersection over union).
- `IMG_SIZE`: 1280 (model input size).

### imagecreation.py

Generates edited versions of images with enhanced greenery using OpenAI's image editing capabilities.

## Configuration

Key settings in `ObjRecognition.py`:

    MODEL_PATH = 'yolov8x-oiv7.pt'      # YOLO model path
    CONF_THRESHOLD = 0.25                # Detection confidence
    IOU_THRESHOLD = 0.45                 # NMS threshold
    IMG_SIZE = 1280                      # Input image size

## Performance Considerations

- **GPU Acceleration**: Uses CUDA if available, falls back to CPU.
- **Sliced Inference**: SAHI processes large images in 640×640 overlapping tiles for better accuracy.
- **Augmentation**: YOLOv8 inference includes augmentation for improved detection.

## Output Example
 
```
========== FINAL REPORT ==========
Image: uploads/sample.jpg
Location: City Name, Country
Coordinates: lat=40.7128, lon=-74.0060
Green Index: 0.35
Traffic Index: 0.20
Human Index: 0.15
Climate: Temperate, 22°C
Living type: Outdoor
Merged Object Counts:
  Tree            : 5
  Plant           : 3
  Car             : 2
  Person          : 1

AI Response:
[Detailed analysis based on metrics and climate context]
```

## Future Enhancements

- Real-time video stream analysis.
- Batch processing for multiple images.
- Historical trend analysis.
- Mobile app integration.
- Enhanced climate data visualization.
- Custom model training support.

## Contributing

Contributions are welcome! Please ensure code follows project standards and includes appropriate testing.

## License

[Add your license information here]

## Support

For issues, questions, or suggestions, please open an issue on [GitHub](https://github.com/thatoneluckyguy/EarthMatterAI/issues).

## References

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [SAHI - Sliced Aided Hyper Inference](https://github.com/obss/sahi)
- [OpenAI API](https://openai.com/api/)

This revised README provides a comprehensive overview of the EarthMatterAI project, detailing its features, installation instructions, usage, and more, while ensuring clarity and coherence throughout the document.
