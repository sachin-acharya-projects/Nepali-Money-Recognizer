from flask import (
    Flask,
    render_template,
    jsonify,
    url_for,  # Might need in Templates
    request,
)
from werkzeug.utils import secure_filename
import os

app = Flask(
    __name__, static_folder="static", static_url_path="", template_folder="templates"
)
app.config["secret"] = "SECRET_KEY_HERE"
app.config["UPLOAD_FOLDER"] = "uploads"


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

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename)) # Just to be safe, using secure_filename
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    file.save(filepath + ".jpg")

    # Image Prediction Goes Here

    return jsonify({"status": True, "classname": "Hundred"})


if __name__ == "__main__":
    app.run(debug=True)
