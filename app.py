from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Groq
model = ChatGroq(
    api_key=os.environ["GROQ_API_KEY"],
    model="llama3-70b-8192",
    temperature=0.7
)

class TravelRequest(BaseModel):
    source: str
    destination: str
    start_date: str
    end_date: str
    budget: float
    travelers: int
    interests: list[str]
    include_flights: bool = False

class ChatRequest(BaseModel):
    question: str
    travel_plan: str

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")  # Update path to static folder

def get_flight_data(source, destination, start_date):
    try:
        source_code = source.strip().upper()
        dest_code = destination.strip().upper()

        url = "https://serpapi.com/search.json"
        params = {
            "engine": "google_flights",
            "departure_id": source_code,
            "arrival_id": dest_code,
            "outbound_date": start_date, 
            "type": "2",  # Keep this since you confirmed it works
            "api_key": os.environ["SERP_API_KEY"],
            "currency": "USD",
            "hl": "en"
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise Exception(f"SerpAPI Error: {response.status_code} - {response.text}")

        return response.json()

    except Exception as e:
        print(f"❌ Error fetching flight data: {str(e)}")
        return None

def format_flight_details_markdown(flight_data, source_code, dest_code, start_date):
    if not flight_data or "best_flights" not in flight_data:
        return "No flights available for this route."

    # Create a single consolidated table with all information
    markdown = "## Available Flight Options\n\n"
    markdown += "| Airline | Flight(s) | Departure | Arrival | Duration | Price | Features | Booking |\n"
    markdown += "|---------|-----------|-----------|---------|----------|-------|----------|--------|\n"

    for option in flight_data["best_flights"][:3]:
        first_flight = option["flights"][0]
        last_flight = option["flights"][-1]

        flight_numbers = " + ".join([f"{flight['airline']} {flight['flight_number']}" for flight in option["flights"]])
        departure = f"{first_flight['departure_airport']['name']} ({first_flight['departure_airport']['time']})"
        arrival = f"{last_flight['arrival_airport']['name']} ({last_flight['arrival_airport']['time']})"
        total_duration = f"{option['total_duration'] // 60}h {option['total_duration'] % 60}m"

        # Format features
        features = set()
        for flight in option["flights"]:
            features.update([ext for ext in flight.get("extensions", []) if "Carbon emissions" not in ext])
        features_str = ", ".join(list(features)[:3])
        
        # Booking link
        booking_link = f"[Book Now](https://www.google.com/flights?hl=en#flt={source_code}.{dest_code}.{start_date})"
        
        # Add layover information to the features column if available
        if "layovers" in option and option["layovers"]:
            layover = option["layovers"][0]
            layover_info = f"Layover: {layover['name']} ({layover['duration'] // 60}h {layover['duration'] % 60}m)"
            features_str = f"{layover_info}<br>{features_str}"

        # Create a complete table row
        markdown += f"| {first_flight['airline']} | {flight_numbers} | {departure} | {arrival} | {total_duration} | ${option['price']} | {features_str} | {booking_link} |\n"

    return markdown

@app.post("/generate-plan")
async def generate_travel_plan(request: TravelRequest):
    try:
        flight_context = ""
        interests_str = ', '.join(request.interests) if request.interests else "General"
        formatted_flight_data = None  # Initialize the variable

        prompt = f"""
        Create a detailed travel plan with the following details:
        From: {request.source}
        To: {request.destination}
        Dates: {request.start_date} to {request.end_date}
        Budget: ${request.budget}
        Number of Travelers: {request.travelers}
        Interests: {interests_str}

        Please provide:
        1. Day-by-day itinerary
        2. Estimated costs breakdown
        3. Recommended accommodations
        4. Must-visit places based on the interests
        5. Local transportation options
        6. Food recommendations
        7. Tips and precautions
        """

        # Get flight details if requested
        if request.include_flights:
            flight_data = get_flight_data(request.source, request.destination, request.start_date)
            if flight_data:
                formatted_flight_data = format_flight_details_markdown(
                    flight_data,
                    request.source.strip().upper(),
                    request.destination.strip().upper(),
                    request.start_date
                )
                prompt += f"\n\nFlight Details:\n{formatted_flight_data}"

        # LangChain call using ChatGroq
        response = model.invoke([HumanMessage(content=prompt)])

        return {
            "success": True,
            "plan": response.content,
            "flight_details": formatted_flight_data if request.include_flights else None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/chat")
async def chat_with_plan(request: ChatRequest):
    try:
        prompt = f"""
        Given this travel plan:
        {request.travel_plan}

        Please answer this question about the plan:
        {request.question}

        Provide a clear and concise response in markdown format.
        """

        response = model.invoke([HumanMessage(content=prompt)])
        return {
            "success": True,
            "response": response.content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")
