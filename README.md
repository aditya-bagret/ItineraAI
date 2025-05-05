# ItineraAI - AI-Powered Trip Planner


ItineraAI is an intelligent travel planning application that leverages AI to create personalized trip itineraries based on user preferences, budget, and travel dates. The platform includes a chatbot travel assistant to help users refine their plans and get travel recommendations.

## ✨ Features

### 🧳 Trip Planning & Management
- **AI-Generated Itineraries**: Create personalized day-by-day travel plans using Groq AI
- **Trip Dashboard**: View, edit, and manage all your planned trips
- **Detailed Itineraries**: Get recommendations for morning, afternoon, evening activities, meals, and accommodations
- **Budget Tracking**: Set and monitor your travel budget

### 🏨 Booking Management
- **Centralized Booking System**: Track all your travel bookings in one place
- **Multiple Booking Types**: Support for flights, hotels, car rentals, activities, and more
- **Confirmation Tracking**: Store confirmation numbers and booking details

### 🤖 AI Travel Assistant
- **Intelligent Chatbot**: Get travel advice, recommendations, and answers to your questions
- **Context-Aware Responses**: The assistant remembers your conversation history
- **Travel-Focused**: Optimized for travel-related queries and planning assistance

### 📝 Reviews & Ratings
- **Trip Reviews**: Share your experiences and rate destinations
- **Community Feedback**: Mark helpful reviews to improve visibility
- **Top Destinations**: Discover highly-rated travel spots

### 🌦️ Weather Integration
- **Current Conditions**: Check weather at your destination
- **Forecast Data**: Plan activities based on upcoming weather
- **Weather Caching**: Efficient data storage for quick access

## 🛠️ Tech Stack

### Frontend
- **HTML/CSS/JavaScript**: Responsive and interactive user interface
- **Bootstrap**: Modern and mobile-friendly design components

### Backend
- **Python 3.x**: Core programming language
- **Flask 2.3.3**: Web framework for building the application
- **Jinja2 3.1.2**: Template engine for dynamic HTML rendering

### Database
- **MySQL**: Relational database for storing user data, trips, bookings, and reviews
- **Flask-MySQLdb**: MySQL database integration for Flask

### AI & External Services
- **Groq API**: AI model integration for itinerary generation and chatbot functionality
- **Weather API**: Real-time weather data for destinations

### Security
- **Flask-Bcrypt**: Password hashing and security
- **Session Management**: Secure user authentication and authorization

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL Server 8.0 or higher
- Groq API key (for AI features)
- Weather API key (for weather integration)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/aditya-bagret/ItineraAI.git
cd ItineraAI
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory with the following variables:
```
# Database Configuration
MYSQL_HOST=localhost
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=trip_planner2

# Application Settings
SECRET_KEY=your_secret_key
DEBUG=True
PORT=5000

# API Keys
GROQ_API_KEY=your_groq_api_key
WEATHER_API_KEY=your_weather_api_key

# Database Initialization (set to True only when you want to initialize the database)
INIT_DB=False
```

### 5. Initialize the Database
```bash
# Set INIT_DB=True in your .env file for first run
python run.py
```

### 6. Run the Application
```bash
python run.py
```

### 7. Access the Application
Open your browser and navigate to:
```
http://localhost:5000
```

## 📁 Project Structure

```
ItineraAI/
├── app.py                  # Main application file
├── extensions.py           # Flask extensions and configurations
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── database/
│   ├── init_db.py          # Database initialization script
│   └── schema.sql          # Database schema
├── routes/
│   ├── api_routes.py       # API endpoints
│   ├── auth_routes.py      # Authentication routes
│   ├── booking_routes.py   # Booking management routes
│   ├── chatbot_routes.py   # Chatbot functionality
│   ├── review_routes.py    # Review management routes
│   ├── trip_routes.py      # Trip management routes
│   └── weather_routes.py   # Weather data routes
├── static/
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   └── images/             # Image assets
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   ├── index.html          # Homepage
│   ├── login.html          # Login page
│   └── ...                 # Other templates
└── utils/                  # Utility functions
    ├── auth_utils.py       # Authentication utilities
    ├── itinerary_generator.py # AI itinerary generation
    └── ...                 # Other utilities
```



## 🔄 API Endpoints

The application provides several API endpoints for integration with other services:

- `/api/trips`: Manage trips programmatically
- `/api/bookings`: Access booking information
- `/api/reviews`: Get review data
- `/api/weather`: Retrieve weather information
- `/chat`: Interact with the AI assistant

## 🔒 Security Features

- Password hashing with bcrypt
- Secure session management
- Input validation and sanitization
- CSRF protection
- Parameterized SQL queries to prevent injection

## 🧪 Testing

To run the tests:
```bash
# Coming soon
```

## 🛣️ Roadmap

### Short-term
- Add map integration for visualizing trip locations
- Implement drag-and-drop functionality for reordering activities
- Enhance mobile responsiveness

### Medium-term
- Add social sharing features for trips
- Implement direct integration with booking APIs
- Add multi-language support

### Long-term
- Develop mobile applications (iOS/Android)
- Implement machine learning for personalized recommendations
- Add virtual reality previews of destinations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📊 Architecture Diagram

<img src="https://i.postimg.cc/qvVGZ4FM/image.png" width="400">

## 📊 E-R Diagram

<img src="https://i.postimg.cc/gj1KpWks/ER-Diagram.png" width="400">

## 📊 Relational Diagram

<img src="https://i.postimg.cc/wvGX5pJz/image.png" width="400">

## 🎨 Project Poster

<img src="https://i.postimg.cc/d1HBWCbz/AI-Travel-Planner.png" width="400">


Check out our project poster [here](https://www.canva.com/design/DAGmPRo8ICc/11QS-4vcVJiY22jfRLAYEg/edit?utm_content=DAGmPRo8ICc&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton).

---

## 📞 Contact

For questions or support, please contact [Aditya](mailto:adityasharma4work@gmail.com).

Happy traveling with ItineraAI! ✈️🌍
