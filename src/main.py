from flask import Flask, request, jsonify, abort
from datetime import datetime
import redis
import json
import logging
import re
import os
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter
from flask_cors import CORS

app = Flask(__name__)
metrics = PrometheusMetrics(app)
CORS(app)

# Connect to local Redis instance with connection pool
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = int(os.getenv('REDIS_PORT', 6379))

pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=0)
r = redis.Redis(connection_pool=pool)

logging.basicConfig(level=logging.INFO)

# Prometheus Counter for birthday messages
birthday_counter = Counter('birthday_messages', 'Total number of birthday messages generated')

def is_valid_username(username):
    return re.match("^[a-zA-Z]+$", username) is not None

def is_valid_date_of_birth(date_of_birth):
    try:
        dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        return dob < datetime.today().date()
    except ValueError:
        return False

@app.errorhandler(400)
def bad_request(error):
    return jsonify(error=str(error)), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify(error=str(error)), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify(error="An unexpected error occurred. Please try again later."), 500

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.route('/hello/<username>', methods=['PUT'])
def update_user(username):
    if not is_valid_username(username):
        logging.error(f"Invalid username: {username}")
        abort(400, "Invalid username. It must contain only letters.")

    if not request.is_json:
        logging.error("Invalid content type. Expected application/json.")
        abort(400, "Invalid content type. Expected application/json.")

    data = request.get_json()
    date_of_birth = data.get('dateOfBirth')

    if not date_of_birth:
        logging.error("Missing dateOfBirth in request data.")
        abort(400, "Missing dateOfBirth in request data.")

    if not is_valid_date_of_birth(date_of_birth):
        logging.error(f"Invalid date of birth: {date_of_birth}")
        abort(400, "Invalid date of birth. It must be in the format YYYY-MM-DD and be a date before today.")

    user_data = {
        "date_of_birth": date_of_birth
    }
    r.set(username, json.dumps(user_data))
    logging.info(f"User {username} updated with date of birth: {date_of_birth}")
    return '', 200

@app.route('/hello/<username>', methods=['GET'])
def get_user_birthday_message(username):
    if not is_valid_username(username):
        logging.error(f"Invalid username: {username}")
        abort(400, "Invalid username. It must contain only letters.")

    user_data = r.get(username)
    
    if not user_data:
        logging.error(f"User {username} not found.")
        abort(404, "User not found.")

    user_data = json.loads(user_data)
    dob = datetime.strptime(user_data['date_of_birth'], '%Y-%m-%d').date()
    
    today = datetime.today().date()
    next_birthday = dob.replace(year=today.year)

    if next_birthday < today:
        next_birthday = next_birthday.replace(year=today.year + 1)

    days_until_birthday = (next_birthday - today).days

    if days_until_birthday == 0:
        message = f"Hello, {username}! Happy birthday!"
    else:
        message = f"Hello, {username}! Your birthday is in {days_until_birthday} day(s)."

    # Increment the birthday message counter
    birthday_counter.inc()

    logging.info(f"Birthday message for {username}: {message}")
    return jsonify(message=message), 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
