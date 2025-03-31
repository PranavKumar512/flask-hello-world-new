from flask import Flask, request, jsonify
import os
from questions import *

app = Flask(__name__)

# Create the 'file' directory if it doesn't exist
os.makedirs("file", exist_ok=True)

# ✅ GET route at `/` to return "Hello, World!"
@app.route("/", methods=["GET"])
def hello_world():
    return jsonify({"message": "Hello, World!"})

# ✅ POST route at `/upload` to handle file upload and question solving
@app.route("/upload", methods=["POST"])
async def upload_file():
    question = request.form.get("question")
    file = request.files.get("file")

    # Handle the file upload
    file_location = None
    if file:
        file_location = os.path.join("file", file.filename)
        file.save(file_location)
        print(f"Saved File: {file_location} ({os.path.getsize(file_location)} bytes)")

    # ✅ Solve the question (await the coroutine)
    result = await solve_question(question, file_location)

    # ✅ Return the answer in JSON format
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
