import openai
import xlwings as xw
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

EXCEL_FILE_PATH = r"C:\Pythonprojects2\buildingdata1.xlsx"

# Set OpenAI API Key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/process-input', methods=['POST'])
def process_input():
    try:
        data = request.json
        location = data.get("location")
        building_type = data.get("building_type")
        area = data.get("area")
        no_of_floors_above = data.get("no_of_floors_above")
        no_of_floors_below = data.get("no_of_floors_below")

        # Open Excel workbook
        app = xw.App(visible=False)
        workbook = xw.Book(EXCEL_FILE_PATH)
        sheet = workbook.sheets["Design"]

        # Write input data
        sheet["D50"].value = location
        sheet["D56"].value = building_type
        sheet["D60"].value = area
        sheet["D62"].value = no_of_floors_above
        sheet["D63"].value = no_of_floors_below

        # Force recalculation & fetch result
        workbook.app.calculate()
        result = sheet["D53"].value

        # Save and close workbook
        workbook.save(EXCEL_FILE_PATH)
        workbook.close()
        app.quit()

        return jsonify({"result": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
