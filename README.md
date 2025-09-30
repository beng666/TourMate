# TourMate Chatbot

TourMate is an innovative chatbot application that uses voice commands and GPS data to provide tourists with personalized route recommendations. It is designed to meet tourists’ instant information needs and enrich their travel experiences.

## Features

1. Voice Command Recognition – Understands and responds to user voice inputs.
2. GPS-Based Route Suggestions – Recommends tourist spots based on the user’s current location.
3. Dynamic Route Planning – Creates personalized routes using real-time GPS data.
4. Instant Information – Provides accurate and up-to-date answers to user queries.

## Kullanılan Teknolojiler

1. T3 AI Model – AI infrastructure provided by T3 AI.
2. Google Geocoding API – Processes and interprets geolocation data.
3. Flask Framework – Backend web application framework.
4. SpeechRecognition Library – Recognizes and processes voice commands.
5. OpenWeather API – Provides real-time weather data.

## Team
- 👤 Bengisu ATLI
- 👤 Deniz TAŞ

## UScreenshots

![WhatsApp Image 2024-09-07 at 11 23 57](https://github.com/user-attachments/assets/88420906-5f16-42f3-9512-3e1bbf1fe02f)

![WhatsApp Image 2024-09-07 at 11 23 57 (1)](https://github.com/user-attachments/assets/439a142d-30ef-42f7-bb89-c5cc1dace26a)

### Installation & Setup

Clone the repository:

   ```bash
   git clone https://github.com/bengssy/TourMate.git
   cd TourMate
```

Create and activate virtual environment:

   ```bash
   python -m venv venv

   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Set environment variables (create a .env file or export manually):

```bash
T3AI_API_KEY=YOUR_T3AI_API_KEY
GOOGLE_GEOCODE_API_KEY=YOUR_GOOGLE_GEOCODE_API_KEY
```

Run the application:

```bash
python app.py
```

📜 License

This project is licensed under the MIT License. See the LICENSE file for details.


