from flask import Flask, request, make_response
from redis import Redis
import os
import socket
import random
import json
import logging
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Redis configuration
redis_password = os.getenv('REDIS_PASSWORD')
redis_host = "redis"

# Helper function to get Redis connection
def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host=redis_host, db=0, socket_timeout=5, password=redis_password)
    return g.redis

# Main route
@app.route("/", methods=['POST', 'GET'])
def hello():
    # Generate a voter ID if not present in cookies
    voter_id = request.cookies.get('id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    # Handle POST request (voting)
    if request.method == 'POST':
        # Get Redis connection
        redis = get_redis()
        
        # Get vote data from the form
        vote = request.form['vote']
        
        # Log the vote received
        logger.info('Received vote for %s', vote)
        
        # Serialize vote data to JSON
        data = json.dumps({'id': voter_id, 'vote': vote})
        
        # Push vote data to Redis queue
        redis.rpush('votes', data)

    # Render the template with options and vote data
    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    
    # Set voter ID cookie
    resp.set_cookie('id', voter_id)
    
    return resp

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
