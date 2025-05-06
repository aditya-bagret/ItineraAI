from flask import Flask, render_template, url_for, request, jsonify, session
from extensions import create_app, mysql
from flask_cors import CORS
import os
from extensions import create_app, mysql, bcrypt, groq_client
from datetime import datetime, timedelta

# Create Flask app
app = create_app()

# Enable CORS for the /chat endpoint
CORS(app, resources={r"/chat": {"origins": "*"}})

# Import routes (after app is created to avoid circular imports)
from routes.auth_routes import auth_bp
from routes.trip_routes import trip_bp
from routes.booking_routes import booking_bp
from routes.weather_routes import weather_bp
from routes.review_routes import review_bp
from routes.api_routes import api_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(trip_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(weather_bp)
app.register_blueprint(review_bp)
app.register_blueprint(api_bp)

# Context processor to make variables available to all templates
@app.context_processor
def inject_now():
    return {
        'now': datetime.now(),
        'timedelta': timedelta
    }

@app.route('/')
def index():
    return render_template('index.html')

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Chatbot functionality
# Fetch recent conversation history from MySQL
def get_conversation_history(user_id, limit=10):
    try:
        cursor = mysql.connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT role, content FROM chat_history WHERE user_id = %s ORDER BY timestamp DESC LIMIT %s",
            (user_id, limit)
        )
        history = cursor.fetchall()
        cursor.close()
        # Reverse to chronological order
        return [{"role": msg["role"], "content": msg["content"]} for msg in reversed(history)]
    except Exception as e:
        print(f"Error fetching history: {e}")
        return []

# Save message to MySQL
def save_message(user_id, role, content):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO chat_history (user_id, role, content, timestamp) VALUES (%s, %s, %s, %s)",
            (user_id, role, content, datetime.utcnow())
        )
        mysql.connection.commit()
        cursor.close()
        print('Chat message saved successfully')
    except Exception as e:
        print(f"Error saving message: {e}")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    print('Received chat request:', data)

    # Validate request data
    if not data or 'message' not in data or 'user_id' not in data:
        return jsonify({'error': 'Invalid request: message and user_id required'}), 400

    user_message = data.get('message')
    user_id = data.get('user_id', 'guest')  # Adjust based on your auth system

    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        # Check if groq_client is initialized
        if groq_client is None:
            print('Groq client not initialized')
            return jsonify({'error': 'Groq client not initialized'}), 500

        # Get conversation history
        history = get_conversation_history(user_id)

        # System prompt for travel context
        system_message = {
            'role': 'system',
            'content': 'You are a travel assistant for an AI travel planner. Answer travel-related questions concisely and accurately, covering destinations, activities, accommodations, or planning tips. For non-travel questions, politely redirect to travel topics.'
        }

        # Combine messages
        messages = [system_message] + history + [{'role': 'user', 'content': user_message}]

        # Call Groq API
        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model='llama3-8b-8192',
            temperature=0.7,
            max_tokens=500
        )

        response = chat_completion.choices[0].message.content
        print('Groq response:', response)

        # Save messages to database
        save_message(user_id, 'user', user_message)
        save_message(user_id, 'assistant', response)

        return jsonify({'response': response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal server error: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG', 'True').lower() == 'true')