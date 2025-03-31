import pandas as pd
import zipfile
import os
import asyncio
import re
import numpy as np
from typing import Optional
from io import BytesIO
from flask import Flask, request, jsonify
from rapidfuzz import fuzz
from GA_1 import (
    get_vscode_open_files,
    extract_email_from_text,
    send_request_and_get_json,
    automate_task,
    run_prettier_and_get_checksum,
    automate_google_sheets_task,
    automate_excel_task,
    automate_day_count_task,
    automate_csv_task,
    extract_and_sort_json,
    automate_hash_task,
    calculate_sum_of_data_values,
    process_zip_and_sum_values,
    create_github_repo_and_push_interactive,
    process_zip_and_replace_text,
    process_zip_and_calculate_size,
    process_zip_and_rename_files,
    process_zip_and_compare_files,
    calculate_total_sales,
)

app = Flask(__name__)

QUESTION_HANDLERS = {
    "get_vscode_open_files": ["What is the output of code -s?"],

    "automate_task": ["Send a HTTPS request to https://httpbin.org/get with the URL encoded parameter email set to 22f3002248@ds.study.iitm.ac.in. What is the JSON output of the command?"],

    "run_prettier_and_get_checksum": ["Run npx -y prettier@3.4.2 README.md | sha256sum. What is the output of the command?"],

    "automate_google_sheets_task": ["What is the result of the Google Sheets formula? =SUM(ARRAY_CONSTRAIN(SEQUENCE(100, 100, 15, 7), 1, 10))."],

    "automate_excel_task": ["What is the result of the Excel formula? =SUM(TAKE(SORTBY({5,9,3,2,14,4,3,1,1,13,2,12,12,11,12,6}, {10,9,13,2,11,8,16,14,7,15,5,4,6,1,3,12}), 1, 9))."],

    "extract_hidden_input_value": ["What is the value in the hidden input?"],

    "automate_day_count_task": ["How many Wednesdays are in the date range 1983-06-08 to 2013-05-08? Include both start and end date."],

    "automate_csv_task": ["Extract CSV file from q-extract-csv-zip.zip and get the 'answer' column."],

    "extract_and_sort_json": ["Sort JSON objects by age, then name."],

    "convert_text_to_json_and_hash": ["Convert text from q-multi-cursor-json.txt into JSON and hash it at tools-in-data-science.pages.dev/jsonhash."],

    "calculate_sum_of_data_values": ["Find all <div>s with class 'foo' and sum their data-value attributes."],

    "process_zip_and_sum_values": ["Process q-unicode-data.zip and sum values for symbols †, Š, … across all files."],

    "create_github_repo_and_push_interactive": ["Create a new GitHub repo and push email.json with {'email': '22f3002248@ds.study.iitm.ac.in'}. Provide the raw GitHub URL."],

    "process_zip_and_replace_text": ["Replace 'IITM' with 'IIT Madras' in q-replace-across-files.zip. What is the sha256sum after running cat * | sha256sum?"],

    "process_zip_and_calculate_size": ["Extract q-list-files-attributes.zip, list files by date and size. Sum sizes of files ≥9552 bytes modified on/after Fri, 10 Nov, 2000, 2:33 AM IST."],

    "process_zip_and_rename_files": ["Move all files into one folder from q-move-rename-files.zip, rename digits (1→2, 9→0). What is the sha256sum after running grep . * | LC_ALL=C sort | sha256sum?"],

    "process_zip_and_compare_files": ["Find the number of differing lines between a.txt and b.txt in q-compress-files.zip."],

    "calculate_total_sales": ["Find total sales of 'Gold' ticket type in a SQLite database. Treat variations (GOLD, gold) as 'Gold'. Sum Units * Price."]
}


def convert_numpy(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(v) for v in obj]
    return obj

async def solve_question(question: str, file_stream: BytesIO = None) -> dict:
    print(f"Received question: {question}")
    await asyncio.sleep(1)

    best_match = None
    best_score = 0

    for handler_name, prompts in QUESTION_HANDLERS.items():
        for prompt in prompts:
            score = fuzz.partial_ratio(prompt.lower(), question.lower())
            if score > best_score:
                best_match = (handler_name, prompt)
                best_score = score

    if best_match and best_score > 50:
        handler_name, prompt = best_match
        handler = globals().get(handler_name)  # Retrieve actual function reference

        if handler is None:
            print(f"Handler function '{handler_name}' not found.")
            return {"answer": "Error: Handler function not found."}

        print(f"Matched prompt: {prompt} with handler: {handler.__name__} (Score: {best_score})")

        if handler in [
            automate_csv_task,
            process_zip_and_sum_values,
            process_zip_and_replace_text,
            process_zip_and_calculate_size,
            process_zip_and_rename_files,
            process_zip_and_compare_files,
        ]:
            answer = handler(question, file_stream)
        else:
            answer = handler(question)

        result = convert_numpy(answer)
        return {"answer": result}

    print("No matching prompt found.")
    return {"answer": "Question not recognized."}


@app.route("/upload", methods=["POST"])
async def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    file_stream = BytesIO(file.read())
    question = request.form.get("question", "")

    result = await solve_question(question, file_stream)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)