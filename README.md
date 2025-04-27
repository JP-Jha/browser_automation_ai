Browser Automation AI:  is an automation tool built using FastAPI and Playwright.
It can automatically:

🌐 Perform deep web searches (with scrolling and extraction)
✈️ Search for flights on Skyscanner based on user input
📧 Login to Gmail accounts automatically

It records the entire browser session (.webm video) and extracts important information (.txt file).
Perfect for automating browser tasks with full evidence capture!

Installation Steps:
 i. Clone the project.
 git clone https://github.com/JP-Jha/browser_automation_ai.git
 cd browser_automation_ai

ii. Create a virtual environment and activate it.
python -m venv myenv
myenv\Scripts\activate  # For Windows
source myenv/bin/activate  # For Mac/Linux

iii. Install all required packages
pip install -r requirements.txt
python -m playwright install

iv. Run the FastAPI server
uvicorn app.main:app --reload

The server will start at:
http://127.0.0.1:8000/docs (Swagger API UI)

Endpoints to Test (Using Postman):
URL: POST http://127.0.0.1:8000/automate
URL: POST http://127.0.0.1:8000/search-flights
URL: POST http://127.0.0.1:8000/gmail-login


#Examples:
Querry for web search:

{
  "url": "https://www.duckduckgo.com",
  "query": "Best tourist places in India"
}

Querry for flight search:

{
  "source": "Delhi",
  "destination": "Patna",
  "departure_date": "2024-06-01",
  "return_date": "2024-06-10",
  "adults": 1,
  "children": 0
}

Querry for gmail search:

{
  "email": "your-email@gmail.com",
  "password": "your-password"
}




