from flask import Flask, request, jsonify
import logging
import pyautogui
import Kinematics
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
@app.route('/')
def hello():
    return "Hello from personNull!"
@app.route('/send_data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()

        if data is None:
            return jsonify({"error": "No data received or invalid JSON"}), 400

        #print(f"Raw data received: {data}")

        if isinstance(data, int):
            return handle_command(data)
        elif isinstance(data, dict) and 'dx' in data and 'dy' in data:
            return handle_movement(data)
        else:
            return jsonify({"error": "Invalid data format"}), 400

    except Exception as e:
        #print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

def handle_command(data):
    commands = {
        0: "Left Click",
        1: "Right Click",
        2: "Scroll Down",
        3: "Scroll Up"
    }

    if data in commands:
        #print(f"Received command: {commands[data]}")
        if data == 0:
            pyautogui.click(button='left')
        elif data == 1:
            pyautogui.click(button='right')
        elif data == 2:
            pyautogui.scroll(10)
        elif data == 3:
            pyautogui.scroll(-10)
        return jsonify({"message": f"{commands[data]} received"}), 200
    else:
        return jsonify({"error": "Invalid command"}), 400

def handle_movement(data):
    dx = data.get('dx')
    dy = data.get('dy')
    if isinstance(dx, (int, float)) and isinstance(dy, (int, float)):
        #print(f"Received movement data: dx={dx}, dy={dy}")
        Kinematics.adjust_mouse(data['dx'], data['dy'])
        return jsonify({"message": "Movement data received successfully", "received": data}), 200
    else:
        return jsonify({"error": "Invalid dx or dy values"}), 400

def run_server():
    app.run(host="0.0.0.0", port=5000)

