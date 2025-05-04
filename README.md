Here’s the updated README with the **tech stack** section added to reflect your use of **Python, MySQL, HTML, CSS, and JavaScript**:

---

# AI Trip Planner

A smart travel planning application that uses AI to generate personalized trip itineraries with additional features like a chatbot travel assistant.

## 🛠 Tech Stack

* **Frontend**: HTML, CSS, JavaScript
* **Backend**: Python (Flask)
* **Database**: MySQL
* **AI Integration**: Groq for itinerary generation
* **APIs**: Weather API, Chatbot assistant

## Frontend Implementation

The frontend has been implemented using:

* HTML
* CSS
* JavaScript

### Directory Structure

```
/static
  /css
    - styles.css (Main CSS file with custom styles)
  /js
    - main.js (JavaScript functionality for interactive elements)
  /images
    - Various image assets for the application

/templates
  - base.html (Base template with common layout elements)
  - index.html (Homepage)
  - login.html (User login)
  - register.html (User registration)
  - profile.html (User profile)
  - trips.html (List of user trips)
  - new_trip.html (Create new trip form)
  - view_trip.html (Detailed trip view with itinerary)
  - 404.html (Not found error page)
  - 500.html (Server error page)
```

### Features Implemented

1. **User Authentication**

   * Login and registration forms
   * User profile management

2. **Trip Management**

   * Create new trips with destination, dates, budget, and preferences
   * View all trips in a grid layout
   * Detailed trip view with day-by-day itinerary
   * Edit, delete, duplicate, and share trips

3. **Itinerary Display**

   * Day-by-day breakdown of activities
   * Morning, lunch, afternoon, dinner, and evening activities
   * Accommodation suggestions

4. **Booking Management**

   * Add and manage bookings for flights, hotels, etc.
   * Track booking details and confirmation numbers

5. **Weather Integration**

   * Display current weather and forecast for the destination

6. **Chatbot Travel Assistant**

   * AI-powered chatbot for assisting with trip planning
   * Provides travel tips, recommendations, and helps with itinerary suggestions

7. **Responsive Design**

   * Mobile-friendly layout
   * Responsive navigation and content display

### How to Run

1. Make sure all required Python packages are installed:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:

   ```bash
   python run.py
   ```

3. Access the application in your browser at:

   ```bash
   http://localhost:5000
   ```

## Backend Integration

The frontend is integrated with the existing Flask backend, which provides:

* User authentication and session management
* Database operations for trips, bookings, and reviews
* AI-powered itinerary generation using Groq
* Weather data integration
* Chatbot integration for travel assistance

## Future Enhancements

* Add more interactive elements to the itinerary planner
* Implement drag-and-drop functionality for reordering activities
* Add a map view for visualizing the trip locations
* Enhance the booking system with direct integration to booking APIs
* Implement social sharing features for trips

---

## Architecture Diagram
![image](https://github.com/user-attachments/assets/a8a30816-4799-4d19-b1ca-afbbbaa9402c)


---

## Poster
https://www.canva.com/design/DAGmPRo8ICc/11QS-4vcVJiY22jfRLAYEg/edit?utm_content=DAGmPRo8ICc&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
