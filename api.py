from flask import Flask, request, jsonify, render_template
from ticket_manager import get_tickets, create_ticket
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return "Ticket System API"

@app.route('/submit_ticket', methods=['GET'])
def submit_ticket():
    app.logger.debug("Rendering submit_ticket.html")
    return render_template('submit_ticket.html')

@app.route('/create_ticket', methods=['POST'])
def create_ticket_route():
    try:
        data = request.form.to_dict()  # Use form data
        app.logger.debug(f"Received data: {data}")  # Debug print
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        result = create_ticket(data)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error: {e}")  # Debug print
        return jsonify({"error": str(e)}), 500

@app.route('/get_tickets', methods=['GET'])
def get_tickets_route():
    try:
        tickets = get_tickets()
        return jsonify(tickets)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)