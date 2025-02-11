import requests

def chatbot_logic(user_input):
    if "process building data" in user_input.lower():
        # Prompt user for details
        print("Bot: Please provide the following details:")
        location = input("Location: ")
        building_type = input("Building Type: ")
        area = float(input("Area (in sq. ft.): "))
        no_of_floors_above = int(input("Number of Floors Above Ground: "))
        no_of_floors_below = int(input("Number of Floors Below Ground: "))

        # Prepare payload
        payload = {
            "location": location,
            "building_type": building_type,
            "area": area,
            "no_of_floors_above": no_of_floors_above,
            "no_of_floors_below": no_of_floors_below
        }

        try:
            # Send data to the Flask API
            response = requests.post('http://127.0.0.1:5000/process-input', json=payload)
            if response.status_code == 200:
                result = response.json().get("result")
                return f"The calculated result is: {result}"
            else:
                return f"Error: {response.json().get('error', 'Unknown error')}"
        except Exception as e:
            return f"Failed to connect to the API: {str(e)}"

    else:
        return "I can help with building data processing. Type 'Process building data' to start."

# Run the chatbot
if __name__ == "__main__":
    print("Chatbot: Hello! How can I assist you today?")
    while True:
        user_message = input("You: ")
        if user_message.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break
        bot_response = chatbot_logic(user_message)
        print(f"Chatbot: {bot_response}")
