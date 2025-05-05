# from flask import Blueprint, request, jsonify
# from app import db, groq_client  # Use app to access db and groq_client from extensions
# from app.models import User, Trip  # Adjust import based on your model location
# from flask_login import current_user
# from datetime import date

# chatbot_bp = Blueprint('chatbot', __name__)

# @chatbot_bp.route('/chatbot/response', methods=['POST'])
# def chatbot_response():
#     data = request.get_json()
#     message = data.get('message', '').lower()

#     if not current_user.is_authenticated:
#         return jsonify({'response': 'Please log in to use the chatbot.'})

#     # Fetch context from user data (e.g., upcoming trips)
#     trips = Trip.query.filter_by(user_id=current_user.id, start_date__gte=date.today()).all()
#     trip_context = 'You have no upcoming trips.' if not trips else f'Your upcoming trips are: {", ".join([t.destination for t in trips])}.'

#     # Prepare prompt with context
#     prompt = f"Based on the following context: {trip_context}. User query: {message}. Provide a helpful response related to trip planning. If the query is unrelated, suggest asking about trips, reviews, or profile."

#     # Call Groq API
#     try:
#         response = groq_client.chat.completions.create(
#             messages=[
#                 {"role": "system", "content": "You are a helpful trip planning assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             model="llama-3.3-70b-versatile",  # Use a supported Groq model
#             max_tokens=500,
#             temperature=0.7
#         )
#         bot_response = response.choices[0].message.content.strip()
#         return jsonify({'response': bot_response})

#     except Exception as e:
#         return jsonify({'response': f'Error connecting to Groq API: {str(e)}'})