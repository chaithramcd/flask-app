import openai
import xlwings as xw
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

EXCEL_FILE_PATH = r"C:\Pythonprojects2\buildingdata1.xlsx"

# Set your OpenAI API Key
openai.api_key = "your_openai_api_key"

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

        # Force recalculation and get result
        workbook.app.calculate()
        result = sheet["D53"].value

        # Save and close workbook
        workbook.save(EXCEL_FILE_PATH)
        workbook.close()
        app.quit()

        # Send result to ChatGPT for explanation
        chatgpt_response = get_chatgpt_response(result)

        return jsonify({"result": result, "chatgpt_explanation": chatgpt_response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_chatgpt_response(input_value):
    """Send the Excel result to ChatGPT for explanation."""
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"The calculated result is {input_value}. Can you explain what it means?",
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error from ChatGPT: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
