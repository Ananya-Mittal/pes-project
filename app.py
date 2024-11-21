from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import hashlib
import random
import time

# Create Flask app
app = Flask(_name_)
CORS(app)
app.config['SECRET_KEY'] = 'cyber-incident-secret'
socketio = SocketIO(app)

# In-memory database for cyber incidents
cyber_incidents = []

# Rate limiting
RATE_LIMIT = 10  # Max requests per IP per minute
requests_log = {}

# Home route serving the main page
@app.route('/')
def index():
    return render_template('index.html')

# SocketIO event handling
@socketio.on('connect')
def handle_connect():
    emit('connected', {'message': 'Connected to the server!'})

@socketio.on('report_incident')
def handle_report(data):
    ip_address = request.remote_addr
    current_time = time.time()

    # Rate limiting logic
    if ip_address not in requests_log:
        requests_log[ip_address] = []

    # Remove requests older than 1 minute
    requests_log[ip_address] = [ts for ts in requests_log[ip_address] if current_time - ts < 60]

    if len(requests_log[ip_address]) >= RATE_LIMIT:
        emit('error', {'message': 'Rate limit exceeded. Try again later.'})
        return

    # Log this request
    requests_log[ip_address].append(current_time)

    # Validate data
    if not data or 'incident_type' not in data or 'description' not in data:
        emit('error', {'message': 'Missing required fields.'})
        return

    # Save the incident
    incident_id = hashlib.sha256(str(random.random()).encode()).hexdigest()
    data['incident_id'] = incident_id
    cyber_incidents.append(data)

    # Broadcast the new incident to all connected clients
    emit('new_incident', data, broadcast=True)

# Fetch all incidents on demand
@socketio.on('get_incidents')
def handle_get_incidents():
    emit('all_incidents', cyber_incidents)

if _name_ == '_main_':
    socketio.run(app, debug=True)