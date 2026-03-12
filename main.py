from flask import Flask, render_template, jsonify, request
import GettingFile
import ObjRecognition
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get-path", methods=["POST"])
def get_path():
    IMG_PATH = GettingFile.Save_Root()
    return jsonify({"path": IMG_PATH})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


