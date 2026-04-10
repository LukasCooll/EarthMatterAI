from flask import Flask, render_template, request, jsonify
import os
import ObjRecognition

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("image")
    if not file or file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    living_type = request.form.get("living_type", "Indoor")
    prompt = request.form.get("prompt")

    result = ObjRecognition.run_detection(path, living_type=living_type, prompt=prompt)
    green_index = result["green_index"]
    traffic_index = result["traffic_index"]
    human_index = result["human_index"]
    annotated_image_path = os.path.join("results", os.path.basename(path))


    annotated_image_b64 = ObjRecognition.get_annotated_image_base64(result["results"])


    return jsonify({
        "image_path": path,
        "annotated_image_path": annotated_image_path,
        "annotated_image": annotated_image_b64,
        "result": {
            "ai_response": result["ai_response"]
        },
        "green_index": green_index,
        "traffic_index": traffic_index,
        "human_index": human_index
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)