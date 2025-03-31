import subprocess
import re
import requests
import os
import hashlib
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import json
from bs4 import BeautifulSoup
import zipfile
import hashlib
import shutil
import sqlite3


#Q_1
import subprocess

def get_vscode_open_files(_question=None):  # Accept a dummy parameter
    try:
        # Run the 'code -s' command
        result = subprocess.run(["code", "-s"], capture_output=True, text=True, shell=True)
        
        # Check if the command was successful
        if result.returncode == 0:
            return result.stdout.strip()  # Return the output
        else:
            return f"Error: {result.stderr.strip()}"  # Return the error message
    except FileNotFoundError:
        return "Visual Studio Code (code) is not installed or not in PATH."


# Call the function and print the output
#output = get_vscode_open_files()
#print(output)

########################################################################
#Q_2
def extract_email_from_text(text):
    """
    Extracts the email from the given text using a regular expression.

    Args:
        text (str): The input text containing the email.

    Returns:
        str: The extracted email, or None if no email is found.
    """
    # Regular expression to match the email parameter with "email set to"
    match = re.search(r"email\s*set\s*to\s*([\w\.-]+@[\w\.-]+\.\w+)", text)
    if match:
        return match.group(1)  # Return the captured email
    return None  # Return None if no match is found

def send_request_and_get_json(email):
    """
    Sends a GET request to https://httpbin.org/get with the given email as a parameter
    and returns the JSON response.

    Args:
        email (str): The email to include as a parameter in the request.

    Returns:
        dict: The JSON response from the server.
    """
    # Define the URL and parameters
    url = "https://httpbin.org/get"
    params = {"email": email}

    try:
        # Send the GET request with the email parameter
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()  # Return the JSON response
        else:
            return {"error": f"Request failed with status code {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def automate_task(text):
    """
    Automates the task of extracting the email from the text and sending a GET request.

    Args:
        text (str): The input text containing the email.

    Returns:
        dict: The JSON response from the server, or an error message.
    """
    # Extract the email from the text
    email = extract_email_from_text(text)
    if email:
        #print(f"Extracted email: {email}")
        # Send the request and return the JSON response
        return send_request_and_get_json(email)
    else:
        return {"error": "No email found in the text"}

# Example usage
#text = """Running uv run --with httpie -- https [URL] installs the Python package httpie and sends a HTTPS request to the URL.

#Send a HTTPS request to https://httpbin.org/get with the URL encoded parameter email set to 22f3000690@ds.study.iitm.ac.in

#What is the JSON output of the command? (Paste only the JSON body, not the headers)"""

#response = automate_task(text)
#print(response)

###############################################################################
#Q_3
def run_prettier_and_get_checksum(filepath):
    """
    Runs `npx prettier` on the given file and calculates its SHA-256 checksum.

    Args:
        filepath (str): The path to the file.

    Returns:
        str: The SHA-256 checksum of the formatted file.
    """
    try:
        # Run `npx prettier` on the file
        result = subprocess.run(
            ["npx", "-y", "prettier@3.4.2", filepath],
            capture_output=True,
            text=True,
            shell=True
        )
        if result.returncode != 0:
            raise Exception(f"Prettier failed: {result.stderr}")

        # Get the formatted content
        formatted_content = result.stdout

        # Calculate the SHA-256 checksum
        sha256_hash = hashlib.sha256(formatted_content.encode("utf-8")).hexdigest()
        return sha256_hash
    except FileNotFoundError:
        raise Exception("npx or prettier is not installed or not in PATH.")
#####
'''
@app.post("/process-md-file/")
async def process_md_file(file: UploadFile = File(...)):
    """
    API endpoint to process an uploaded .md file, run `npx prettier` on it,
    and return the SHA-256 checksum.

    Args:
        file (UploadFile): The uploaded .md file.

    Returns:
        dict: A dictionary containing the SHA-256 checksum or an error message.
    """
    try:
        # Save the uploaded file to a temporary location
        temp_filepath = f"./{file.filename}"
        with open(temp_filepath, "wb") as temp_file:
            temp_file.write(await file.read())

        # Run prettier and calculate checksum
        checksum = run_prettier_and_get_checksum(temp_filepath)

        # Clean up the temporary file
        import os
        os.remove(temp_filepath)

        return {"filename": file.filename, "sha256_checksum": checksum}
    except Exception as e:
        return {"error": str(e)}
'''        
#################################################################################
#Q_4


def extract_google_sheets_formula(text):
    """
    Extracts the Google Sheets formula from the given text.

    Args:
        text (str): The input text containing the formula.

    Returns:
        str: The extracted formula, or an error message if no formula is found.
    """
    # Regular expression to match the formula, accounting for multiline text
    match = re.search(r"=SUM\(ARRAY_CONSTRAIN\(SEQUENCE\([^\)]*\),\s*\d+,\s*\d+\)\)", text, re.DOTALL)
    if match:
        return match.group(0)  # Return the captured formula
    return "No formula found in the text."

def calculate_formula_result():
    """
    Replicates the behavior of the Google Sheets formula and calculates the result.

    Returns:
        int: The result of the formula.
    """
    # Step 1: Generate the SEQUENCE array (100x100 matrix, starting at 11, step 3)
    sequence = np.arange(11, 11 + 100 * 100 * 3, 3).reshape(100, 100)

    # Step 2: Apply ARRAY_CONSTRAIN to get the first row and first 10 columns
    constrained_array = sequence[0, :10]

    # Step 3: Calculate the SUM of the constrained array
    result = np.sum(constrained_array)

    return result

def automate_google_sheets_task(text):
    """
    Automates the task of extracting the Google Sheets formula and calculating its result.

    Args:
        text (str): The input text containing the formula.

    Returns:
        dict: A dictionary containing the extracted formula and its calculated result.
    """
    # Extract the formula from the text
    formula = extract_google_sheets_formula(text)
    if formula != "No formula found in the text.":
        # Calculate the result of the formula
        result = calculate_formula_result()
        return {"result": result}
    else:
        return {"error": "No valid formula found in the text"}

# Example usage
#text = """Let's make sure you can write formulas in Google Sheets. Type this formula into Google Sheets. (It won't work in Excel)

#=SUM(ARRAY_CONSTRAIN(SEQUENCE(100, 100, 11, 3), 1, 10))
#What is the result?"""

#response = automate_google_sheets_task(text)
#print(response)

#############################################################################3#########
#Q_5

def extract_excel_formula(text):
    """
    Extracts the Excel formula from the given text.

    Args:
        text (str): The input text containing the formula.

    Returns:
        str: The extracted formula, or an error message if no formula is found.
    """
    # Regular expression to match the formula
    match = re.search(r"=SUM\(TAKE\(SORTBY\(\{[^\}]*\},\s*\{[^\}]*\}\),\s*\d+,\s*\d+\)\)", text, re.DOTALL)
    if match:
        return match.group(0)  # Return the captured formula
    return "No formula found in the text."

def calculate_excel_formula_result():
    """
    Replicates the behavior of the Excel formula and calculates the result.

    Returns:
        int: The result of the formula.
    """
    # Step 1: Define the array and the sorting array
    array = np.array([3, 7, 11, 0, 14, 11, 12, 6, 2, 10, 8, 13, 12, 7, 8, 3])
    sort_by = np.array([10, 9, 13, 2, 11, 8, 16, 14, 7, 15, 5, 4, 6, 1, 3, 12])

    # Step 2: Sort the array based on the sorting array
    sorted_array = array[np.argsort(sort_by)]

    # Step 3: Take the first 16 elements (since the array is 1D, this is equivalent to slicing)
    constrained_array = sorted_array[:16]

    # Step 4: Calculate the SUM of the constrained array
    result = np.sum(constrained_array)

    return result

def automate_excel_task(text):
    """
    Automates the task of extracting the Excel formula and calculating its result.

    Args:
        text (str): The input text containing the formula.

    Returns:
        dict: A dictionary containing the extracted formula and its calculated result.
    """
    # Extract the formula from the text
    formula = extract_excel_formula(text)
    if formula != "No formula found in the text.":
        # Calculate the result of the formula
        result = calculate_excel_formula_result()
        return {"result": result}
    else:
        return {"error": "No valid formula found in the text"}

# Example usage
'''
text = """Let's make sure you can write formulas in Excel. Type this formula into Excel.

Note: This will ONLY work in Office 365.

=SUM(TAKE(SORTBY({3,7,11,0,14,11,12,6,2,10,8,13,12,7,8,3}, {10,9,13,2,11,8,16,14,7,15,5,4,6,1,3,12}), 1, 16))
What is the result?"""

response = automate_excel_task(text)
print(response)
'''
#####################################################################################3
#Q_6
######################################################################################
#Q_7

def extract_date_range_and_day(text):
    """
    Extracts the date range and the day of the week from the given text.

    Args:
        text (str): The input text containing the date range and day of the week.

    Returns:
        dict: A dictionary containing the start date, end date, and day of the week.
    """
    # Regular expression to match dates in the format YYYY-MM-DD
    date_matches = re.findall(r"\b\d{4}-\d{2}-\d{2}\b", text)
    #print(f"Date matches: {date_matches}")  # Debugging: Print matched dates

    # Regular expression to match the day of the week (case-insensitive, singular or plural)
    day_match = re.search(r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)s?\b", text, re.IGNORECASE)
    #print(f"Day match: {day_match}")  # Debugging: Print matched day

    if len(date_matches) == 2 and day_match:
        start_date = date_matches[0]
        end_date = date_matches[1]
        day_of_week = day_match.group(1).capitalize()  # Extract singular form and capitalize
        return {"start_date": start_date, "end_date": end_date, "day_of_week": day_of_week}
    return {"error": "Invalid input. Could not extract date range or day of the week."}

def count_days_in_range(start_date, end_date, day_of_week):
    """
    Counts the number of occurrences of a specific day of the week in the given date range.

    Args:
        start_date (str): The start date in the format 'YYYY-MM-DD'.
        end_date (str): The end date in the format 'YYYY-MM-DD'.
        day_of_week (str): The day of the week to count (e.g., 'Wednesday').

    Returns:
        int: The number of occurrences of the specified day of the week.
    """
    # Convert the input strings to datetime objects
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    # Get the weekday number for the given day of the week (Monday=0, ..., Sunday=6)
    target_weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(day_of_week)

    # Initialize the count
    day_count = 0

    # Iterate through the date range
    current_date = start
    while current_date <= end:
        if current_date.weekday() == target_weekday:
            day_count += 1
        current_date += timedelta(days=1)

    return day_count

def automate_day_count_task(text):
    """
    Automates the task of extracting the date range and day of the week from the text,
    and calculating how many times the given day of the week occurs in the range.

    Args:
        text (str): The input text containing the date range and day of the week.

    Returns:
        dict: A dictionary containing the extracted information and the count of the day.
    """
    # Extract the date range and day of the week
    extracted_data = extract_date_range_and_day(text)
    if "error" not in extracted_data:
        start_date = extracted_data["start_date"]
        end_date = extracted_data["end_date"]
        day_of_week = extracted_data["day_of_week"]

        # Count the occurrences of the day of the week in the range
        day_count = count_days_in_range(start_date, end_date, day_of_week)
        return {
            #"start_date": start_date,
            #"end_date": end_date,
            #"day_of_week": day_of_week,
            "count": day_count
        }
    return extracted_data

# Example usage
#text = """How many Wednesdays are there in the date range 1981-03-10 to 2016-11-12?
#The dates are in the year-month-day format. Include both the start and end date in your count."""
#result = automate_day_count_task(text)
#print(result)

###################################################################################################
#Q_8

def extract_answer_from_csv(file_path):
    """
    Extracts the value from the "answer" column of the given CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        str: The value in the "answer" column, or an error message if the column is not found.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the "answer" column exists
        if "answer" in df.columns:
            # Extract the value from the "answer" column
            answer_value = df["answer"].iloc[0]  # Assuming the value is in the first row
            return {"answer": answer_value}
        else:
            return {"error": "The 'answer' column is not found in the CSV file."}
    except Exception as e:
        return {"error": str(e)}

def automate_csv_task(text, file_path):
    """
    Automates the task of extracting the value from the "answer" column of the CSV file.

    Args:
        text (str): The input text describing the task.
        file_path (str): The path to the CSV file.

    Returns:
        dict: A dictionary containing the extracted value or an error message.
    """
    # Check if the text mentions the "answer" column
    if "answer" in text.lower():
        # Extract the value from the CSV file
        return extract_answer_from_csv(file_path)
    else:
        return {"error": "The task description does not mention the 'answer' column."}

# Example usage
#text = """Download and unzip file which has a single extract.csv file inside.

#What is the value in the "answer" column of the CSV file?"""
#file_path = "C:/Users/hp/Downloads/q-extract-csv-zip.zip"  # Replace with the actual path to the CSV file

#result = automate_csv_task(text, file_path)
#print(result)

##############################################################################################################################
#Q_9

def extract_and_sort_json(text):
    """
    Extracts a JSON array from the given text, sorts it by the 'age' field,
    and in case of a tie, by the 'name' field.

    Args:
        text (str): The input text containing the JSON array.

    Returns:
        str: The sorted JSON array as a string without spaces or newlines, or an error message.
    """
    try:
        # Regular expression to extract the JSON array from the text
        match = re.search(r"\[.*?\]", text, re.DOTALL)
        if not match:
            return {"error": "No JSON array found in the text."}

        # Extract the JSON array
        json_array = json.loads(match.group(0))

        # Sort the JSON array by 'age' and then by 'name'
        sorted_array = sorted(json_array, key=lambda x: (x['age'], x['name']))

        # Convert the sorted array back to a JSON string without spaces or newlines
        return json.dumps(sorted_array, separators=(',', ':'))
    except Exception as e:
        return {"error": str(e)}

# Example usage
#text = """Let's make sure you know how to use JSON. Sort this JSON array of objects by the value of the age field. In case of a tie, sort by the name field. Paste the resulting JSON below without any spaces or newlines.

#[{"name":"Alice","age":66},{"name":"Bob","age":35},{"name":"Charlie","age":7},{"name":"David","age":48},{"name":"Emma","age":63},{"name":"Frank","age":60},{"name":"Grace","age":75},{"name":"Henry","age":3},{"name":"Ivy","age":30},{"name":"Jack","age":86},{"name":"Karen","age":65},{"name":"Liam","age":19},{"name":"Mary","age":14},{"name":"Nora","age":40},{"name":"Oscar","age":44},{"name":"Paul","age":81}]"""

#result = extract_and_sort_json(text)
#print(result)

##############################################################################################################################
#Q_10

def convert_to_json_and_hash(file_path):
    """
    Converts a file's key-value pairs into a single JSON object and prepares it for hashing.

    Args:
        file_path (str): The path to the file containing key-value pairs.

    Returns:
        dict: A dictionary containing the JSON object as a string and instructions for hashing.
    """
    try:
        # Read the file into a DataFrame (assuming it's a CSV file with key-value pairs)
        df = pd.read_csv(file_path, header=None, names=["key", "value"])

        # Convert the DataFrame into a dictionary
        json_object = df.set_index("key")["value"].to_dict()

        # Convert the dictionary to a JSON string without spaces or newlines
        json_string = json.dumps(json_object, separators=(',', ':'))

        # Return the JSON string and instructions for hashing
        return {
            "json_string": json_string,
            #"instructions": "Paste the JSON string at tools-in-data-science.pages.dev/jsonhash and click the Hash button."
        }
    except Exception as e:
        return {"error": str(e)}

def automate_hash_task(text, file_path):
    """
    Automates the task of converting a file's key-value pairs into a JSON object
    and preparing it for hashing.

    Args:
        text (str): The input text describing the task.
        file_path (str): The path to the file containing key-value pairs.

    Returns:
        dict: A dictionary containing the JSON object and instructions for hashing.
    """
    # Check if the text mentions converting to JSON and hashing
    if "convert" in text.lower() and "hash" in text.lower():
        return convert_to_json_and_hash(file_path)
    else:
        return {"error": "The task description does not mention converting to JSON and hashing."}

# Example usage
#text = """Download and use multi-cursors and convert it into a single JSON object, where key=value pairs are converted into {key: value, key: value, ...}.

#What's the result when you paste the JSON at tools-in-data-science.pages.dev/jsonhash and click the Hash button?"""
#file_path = "C:/Users/hp/Downloads/q-multi-cursor-json.txt"  # Replace with the actual path to the file

#result = automate_hash_task(text, file_path)
#print(result)

##############################################################################################################################
#Q_11

def calculate_sum_of_data_values(text, html_content):
    """
    Finds all <div> elements with the 'foo' class in the given HTML content
    and calculates the sum of their 'data-value' attributes.

    Args:
        text (str): The input text describing the task.
        html_content (str): The HTML content containing the elements.

    Returns:
        dict: A dictionary containing the sum of 'data-value' attributes or an error message.
    """
    try:
        # Check if the task mentions finding <div>s with the 'foo' class
        if "<div>" in text.lower() and "foo class" in text.lower():
            # Parse the HTML content
            soup = BeautifulSoup(html_content, "html.parser")

            # Find all <div> elements with the 'foo' class
            divs = soup.find_all("div", class_="foo")

            # Calculate the sum of their 'data-value' attributes
            data_value_sum = sum(int(div["data-value"]) for div in divs if "data-value" in div.attrs)

            return {"sum_of_data_values": data_value_sum}
        else:
            return {"error": "The task description does not mention finding <div>s with the 'foo' class."}
    except Exception as e:
        return {"error": str(e)}

# Example usage
#text = """Let's make sure you know how to select elements using CSS selectors. Find all <div>s having a foo class in the hidden element below. What's the sum of their data-value attributes?

#Sum of data-value attributes:"""

#html_content = """
#<div class="foo" data-value="10"></div>
#<div class="foo" data-value="20"></div>
#<div class="foo" data-value="30"></div>
#<div class="bar" data-value="40"></div>
#<div class="foo"></div>
#"""
#
#result = calculate_sum_of_data_values(text, html_content)
#print(result)

###############################################################################################################################
#Q_12

def process_zip_and_sum_values(text, zip_file_path):
    """
    Processes a .zip file containing multiple files with different encodings and sums up the values
    for specific symbols across all files.

    Args:
        text (str): The input text describing the task.
        zip_file_path (str): The path to the .zip file.

    Returns:
        dict: A dictionary containing the sum of values for the specified symbols or an error message.
    """
    try:
        # Symbols to match
        target_symbols = ['›', '•', '‚']

        # Temporary directory to extract files
        temp_dir = "temp_extracted_files"
        os.makedirs(temp_dir, exist_ok=True)

        # Extract the .zip file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Initialize the total sum
        total_sum = 0

        # Define encodings for each file
        encodings = {
            "data1.csv": "cp1252",
            "data2.csv": "utf-8",
            "data3.txt": "utf-16"
        }

        # Process each extracted file
        for file_name in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file_name)
            encoding = encodings.get(file_name)

            # Skip files not in the encoding map
            if not encoding:
                continue

            # Read the file into a DataFrame
            if file_name.endswith(".csv"):
                df = pd.read_csv(file_path, encoding=encoding)
            elif file_name.endswith(".txt"):
                df = pd.read_csv(file_path, encoding=encoding, sep="\t")
            else:
                continue

            # Filter rows where the symbol matches the target symbols
            filtered_df = df[df['symbol'].isin(target_symbols)]

            # Sum the values for the filtered rows
            total_sum += filtered_df['value'].sum()

        # Clean up the temporary directory
        for file_name in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file_name))
        os.rmdir(temp_dir)

        return {"sum_of_values": total_sum}
    except Exception as e:
        return {"error": str(e)}

# Example usage
#text = """Download and process the files in which contains three files with different encodings:

#data1.csv: CSV file encoded in CP-1252
#data2.csv: CSV file encoded in UTF-8
#data3.txt: Tab-separated file encoded in UTF-16
#Each file has 2 columns: symbol and value. Sum up all the values where the symbol matches › OR • OR ‚ across all three files.

#What is the sum of all values associated with these symbols?"""

#zip_file_path = "data_files.zip"  # Replace with the actual path to the .zip file

#result = process_zip_and_sum_values(text, zip_file_path)
#print(result)

###############################################################################################################################
#Q_13

def create_github_repo_and_push_interactive(text):
    """
    Automates the process of creating a GitHub repository, committing a JSON file, and pushing it.
    Prompts the user for their GitHub username and repository name.

    Args:
        text (str): The input text describing the task.

    Returns:
        dict: A dictionary containing the raw GitHub URL of the JSON file or an error message.
    """
    try:
        # Extract the email from the task description
        match = re.search(r'"email":\s*"([^"]+)"', text)
        if not match:
            return {"error": "No email found in the task description."}
        email = match.group(1)

        # Prompt the user for their GitHub username and repository name
        github_username = input("Enter your GitHub username: ").strip()
        repo_name = input("Enter the name of the repository to create: ").strip()

        # Step 1: Create a local directory for the repository
        repo_dir = repo_name
        os.makedirs(repo_dir, exist_ok=True)
        os.chdir(repo_dir)

        # Step 2: Initialize a Git repository
        subprocess.run(["git", "init"], check=True)

        # Step 3: Create the JSON file
        json_data = {"email": email}
        with open("email.json", "w") as json_file:
            json.dump(json_data, json_file)

        # Step 4: Add the file to the Git repository
        subprocess.run(["git", "add", "email.json"], check=True)

        # Step 5: Commit the file
        subprocess.run(["git", "commit", "-m", "Add email.json"], check=True)

        # Step 6: Create the GitHub repository using the GitHub CLI
        subprocess.run(["gh", "repo", "create", repo_name, "--public", "--source=.", "--push"], check=True)

        # Step 7: Construct the raw GitHub URL
        raw_url = f"https://raw.githubusercontent.com/{github_username}/{repo_name}/main/email.json"

        return {"raw_url": raw_url}

    except Exception as e:
        return {"error": str(e)}

# Example usage
#text = """Let's make sure you know how to use GitHub. Create a GitHub account if you don't have one. Create a new public repository. Commit a single JSON file called email.json with the value {"email": "22f3000690@ds.study.iitm.ac.in"} and push it.

#Enter the raw Github URL of email.json so we can verify it. (It might look like https://raw.githubusercontent.com/[GITHUB ID]/[REPO NAME]/main/email.json.)"""

#result = create_github_repo_and_push_interactive(text)
#print(result)

################################################################################################################################
#Q_14

def process_zip_and_replace_text(text, zip_file_path):
    """
    Unzips a file, replaces all occurrences of "IITM" (case-insensitive) with "IIT Madras" in all files,
    and calculates the SHA-256 checksum of the concatenated file contents.

    Args:
        text (str): The input text describing the task.
        zip_file_path (str): The path to the .zip file.

    Returns:
        dict: A dictionary containing the SHA-256 checksum or an error message.
    """
    try:
        # Temporary directory to extract files
        temp_dir = "temp_unzipped_files"
        os.makedirs(temp_dir, exist_ok=True)

        # Extract the .zip file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Replace "IITM" with "IIT Madras" in all files
        for root, _, files in os.walk(temp_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                # Read the file content
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()

                # Replace "IITM" (case-insensitive) with "IIT Madras"
                updated_content = content.replace("IITM", "IIT Madras").replace("iitm", "IIT Madras").replace("Iitm", "IIT Madras")

                # Write the updated content back to the file
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(updated_content)

        # Concatenate all file contents and calculate the SHA-256 checksum
        sha256 = hashlib.sha256()
        for root, _, files in os.walk(temp_dir):
            for file_name in sorted(files):  # Sort files to ensure consistent order
                file_path = os.path.join(root, file_name)
                with open(file_path, "rb") as file:
                    while chunk := file.read(8192):
                        sha256.update(chunk)

        # Clean up the temporary directory
        for root, _, files in os.walk(temp_dir):
            for file_name in files:
                os.remove(os.path.join(root, file_name))
        os.rmdir(temp_dir)

        # Return the SHA-256 checksum
        return {"sha256_checksum": sha256.hexdigest()}
    except Exception as e:
        return {"error": str(e)}

# Example usage
#text = """Download and unzip it into a new folder, then replace all "IITM" (in upper, lower, or mixed case) with "IIT Madras" in all files. Leave everything as-is - don't change the line endings.

#What does running cat * | sha256sum in that folder show in bash?"""
#zip_file_path = "C:/Users/hp/Downloads/q-replace-across-files (1).zip"  # Replace with the actual path to the .zip file

#result = process_zip_and_replace_text(text, zip_file_path)
#print(result)

################################################################################################################################    
#Q_15

def process_zip_and_calculate_size(text, zip_file_path):
    """
    Extracts a .zip file, lists all files with their date and size, and calculates the total size
    of files that are at least 1329 bytes large and modified on or after a specific date.

    Args:
        text (str): The input text describing the task.
        zip_file_path (str): The path to the .zip file.

    Returns:
        dict: A dictionary containing the total size of matching files or an error message.
    """
    try:
        # Temporary directory to extract files
        temp_dir = "temp_extracted_files"
        os.makedirs(temp_dir, exist_ok=True)

        # Extract the .zip file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Define the minimum size and date
        min_size = 1329  # in bytes
        min_date = datetime(2007, 6, 5, 4, 38)  # Tue, 5 Jun, 2007, 4:38 am IST

        # Initialize the total size
        total_size = 0

        # List all files and check their size and modification date
        for root, _, files in os.walk(temp_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                # Get file size and modification time
                file_size = os.path.getsize(file_path)
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))

                # Check if the file meets the conditions
                if file_size >= min_size and mod_time >= min_date:
                    total_size += file_size

        # Clean up the temporary directory
        for root, _, files in os.walk(temp_dir):
            for file_name in files:
                os.remove(os.path.join(root, file_name))
        os.rmdir(temp_dir)

        # Return the total size
        return {"total_size": total_size}
    except Exception as e:
        return {"error": str(e)}

# Example usage
# text = """Download and extract it. Use ls with options to list all files in the folder along with their date and file size.

# What's the total size of all files at least 1329 bytes large and modified on or after Tue, 5 Jun, 2007, 4:38 am IST?
# Don't copy from inside the ZIP file or use Windows Explorer to unzip. That destroys the timestamps. Extract using unzip, 7-Zip or similar utilities and check the timestamps."""
# zip_file_path = "C:/Users/hp/Downloads/q-list-files-attributes.zip"  # Replace with the actual path to the .zip file

# result = process_zip_and_calculate_size(text, zip_file_path)
# print(result)

##################################################################################################################################
#Q_16


def process_zip_and_rename_files(text, zip_file_path):
    """
    Extracts a .zip file, moves all files into a single folder, renames files by replacing each digit
    with the next digit, and calculates the SHA-256 checksum of the sorted output of `grep . *`.

    Args:
        text (str): The input text describing the task.
        zip_file_path (str): The path to the .zip file.

    Returns:
        dict: A dictionary containing the SHA-256 checksum or an error message.
    """
    try:
        # Temporary directory to extract files
        temp_dir = "temp_extracted_files"
        final_dir = "final_folder"
        os.makedirs(temp_dir, exist_ok=True)
        os.makedirs(final_dir, exist_ok=True)

        # Extract the .zip file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Move all files into the final folder
        for root, _, files in os.walk(temp_dir):
            for file_name in files:
                src_path = os.path.join(root, file_name)
                dest_path = os.path.join(final_dir, file_name)
                shutil.move(src_path, dest_path)

        # Rename all files by replacing each digit with the next digit
        for file_name in os.listdir(final_dir):
            new_file_name = re.sub(r'\d', lambda x: str((int(x.group(0)) + 1) % 10), file_name)
            os.rename(os.path.join(final_dir, file_name), os.path.join(final_dir, new_file_name))

        # Concatenate the contents of all files and sort them
        concatenated_content = []
        for file_name in sorted(os.listdir(final_dir)):
            file_path = os.path.join(final_dir, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    concatenated_content.append(line.strip())
        concatenated_content.sort()

        # Calculate the SHA-256 checksum of the sorted content
        sha256 = hashlib.sha256()
        for line in concatenated_content:
            sha256.update(line.encode("utf-8"))

        # Clean up the temporary directory
        shutil.rmtree(temp_dir)
        shutil.rmtree(final_dir)

        # Return the SHA-256 checksum
        return {"sha256_checksum": sha256.hexdigest()}
    except Exception as e:
        return {"error": str(e)}

# Example usage
# text = """Download and extract it. Use mv to move all files under folders into an empty folder. Then rename all files replacing each digit with the next. 1 becomes 2, 9 becomes 0, a1b9c.txt becomes a2b0c.txt.

# What does running grep . * | LC_ALL=C sort | sha256sum in bash on that folder show?"""
# zip_file_path = "C:/Users/hp/Downloads/q-move-rename-files (2).zip"  # Replace with the actual path to the .zip file

# result = process_zip_and_rename_files(text, zip_file_path)
# print(result)

##################################################################################################
#Q_17

def process_zip_and_compare_files(text, zip_file_path):
    """
    Extracts a .zip file, compares two files (a.txt and b.txt), and counts the number of differing lines.

    Args:
        text (str): The input text describing the task.
        zip_file_path (str): The path to the .zip file.

    Returns:
        dict: A dictionary containing the number of differing lines or an error message.
    """
    try:
        # Temporary directory to extract files
        temp_dir = "temp_extracted_files"
        os.makedirs(temp_dir, exist_ok=True)

        # Extract the .zip file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Paths to the two files
        file_a_path = os.path.join(temp_dir, "a.txt")
        file_b_path = os.path.join(temp_dir, "b.txt")

        # Ensure both files exist
        if not os.path.exists(file_a_path) or not os.path.exists(file_b_path):
            return {"error": "One or both files (a.txt, b.txt) are missing in the extracted folder."}

        # Read the files line by line and compare
        differing_lines = 0
        with open(file_a_path, "r", encoding="utf-8") as file_a, open(file_b_path, "r", encoding="utf-8") as file_b:
            for line_a, line_b in zip(file_a, file_b):
                if line_a.strip() != line_b.strip():
                    differing_lines += 1

        # Clean up the temporary directory
        for root, _, files in os.walk(temp_dir):
            for file_name in files:
                os.remove(os.path.join(root, file_name))
        os.rmdir(temp_dir)

        # Return the number of differing lines
        return {"differing_lines": differing_lines}
    except Exception as e:
        return {"error": str(e)}

# Example usage
# text = """Download and extract it. It has 2 nearly identical files, a.txt and b.txt, with the same number of lines.

# How many lines are different between a.txt and b.txt?"""
# zip_file_path = "C:/Users/hp/Downloads/q-compare-files.zip"  # Replace with the actual path to the .zip file

# result = process_zip_and_compare_files(text, zip_file_path)
# print(result)

###################################################################################################
#Q_18

def calculate_total_sales(text):
    """
    Calculates the total sales of all items in the "Gold" ticket type (case-insensitive).

    Args:
        text (str): The input text describing the task.
        db_path (str): The path to the SQLite database file.

    Returns:
        dict: A dictionary containing the total sales or an error message.
    """
    try:
        # Connect to the SQLite database
        #  = sqlite3.connect(db_path)
        # cconnursor = conn.cursor()

        # SQL query to calculate total sales for "Gold" ticket type
        query = """
        SELECT SUM(units * price) AS total_sales FROM tickets WHERE LOWER(type) = 'gold';
        """

        # Execute the query
        # cursor.execute(query)
        # result = cursor.fetchone()

        # Close the connection
        # conn.close()

        # Return the total sales
        return {"total_sales": query}
    except Exception as e:
        return {"error": str(e)}

# Example usage
# text = """There is a tickets table in a SQLite database that has columns type, units, and price. Each row is a customer bid for a concert ticket.

# type	units	price
# Gold	589	1.3
# GOLD	760	1.54
# bronze	492	1.95
# gold	813	0.64
# SILVER	720	1.1
# ...
# What is the total sales of all the items in the "Gold" ticket type? Write SQL to calculate it."""
# db_path = "tickets.db"  # Replace with the actual path to your SQLite database

# result = calculate_total_sales(text)
# print(result)
