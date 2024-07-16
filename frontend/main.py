from flask import (
    Flask,
    render_template,
    jsonify,
    url_for,  # Might need in Templates
    request,
)
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(
    __name__, static_folder="static", static_url_path="", template_folder="templates"
)
app.config["secret"] = "SECRET_KEY_HERE"
app.config["UPLOAD_FOLDER"] = "uploads"

model = load_model("models/currency_classifier_resnet50.h5")
data_dir = "C:/Users/ACER/Desktop/datasets/dataset/train/"
class_names = sorted(os.listdir(data_dir))


def predict(image_path: str) -> str:
    image_ = image.load_img(image_path, target_size=(224, 224))
    image_array = image.img_to_array(image_)
    image_array = np.expand_dims(image_array, axis=0)
    image_array /= 255

    predictions = model.predict(image_array)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_class_name = class_names[predicted_class_index]
    return predicted_class_name


@app.errorhandler(404)
def handlePageMissing(e):
    return f"<strong>{e}</strong>"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html"), 200

    if "file" not in request.files:
        return jsonify({"status": False, "message": "Request object has no file part"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"status": False, "message": "Please upload an image"})

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"], secure_filename(file.filename)
    )  # Just to be safe, using secure_filename
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    file.save(filepath + ".jpg")

    classname = predict(filepath)
    # Image Prediction Goes Here

    return jsonify({"status": True, "classname": classname})


if __name__ == "__main__":
    app.run(debug=True)
