
# Travel Planning AI

A full-stack AI-powered travel planning application that generates personalized travel itineraries based on user preferences. The application uses Groq's LLaMA 3 model for generating comprehensive travel plans and SerpAPI for fetching flight information.

Try here [https://travelplanner-rl15.onrender.com/](https://travelplanner-rl15.onrender.com/)

## 🌟 Features


Personalized Travel Plans: Generate detailed travel itineraries based on your preferences


Day-by-day Itinerary: Detailed breakdown of activities for each day of your trip


Budget Analysis: Estimated cost breakdown for your entire trip


Accommodation Recommendations: Suggestions for places to stay that fit your budget


Flight Information: Optional integration with real flight data (via SerpAPI)


Interactive Chat: Ask questions about your generated travel plan


Responsive Design: Works well on both desktop and mobile devices


Docker Support: Containerized for easy deployment



## 🛠️ Tech Stack


Frontend: HTML, CSS, JavaScript


Backend: FastAPI (Python)


AI: Groq API (LLaMA 3 70B model)


Flight Data: SerpAPI (Google Flights data)


Containerization: Docker with Nginx for frontend and Python for backend



## 📋 Prerequisites


Docker and Docker Compose (for containerized deployment)


Groq API key


SerpAPI key



## 🚀 Setup &amp; Installation
### Local Development


Clone the repository:
git clone &lt;repo-url&gt;
cd &lt;repo-directory&gt;



Create environment file:
cp .env.example .env



Set up a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate



Install dependencies:
pip install -r requirements.txt



Run the backend:
uvicorn main:app --reload



Access the application:
Open your browser and navigate to http://localhost:8000


### Docker Deployment


Build and run with Docker:
docker-compose up --build



Access the application:
Open your browser and navigate to http://localhost:80



## 📝 Usage


Enter your travel details:


Source location


Destination


Start and end dates


Budget (in USD)


Number of travelers


Your interests (comma-separated)


Optional: Check "Include Flight Details" to see flight options




Generate your travel plan:


Click the "Generate Travel Plan" button


Wait for the AI to create your personalized itinerary




Interact with your plan:


View your day-by-day itinerary


See estimated costs and accommodations


If requested, check flight options


Use the chat feature to ask questions about your plan





## 🌐 Environment Variables


GROQ_API_KEY: Your Groq API key for AI model access


SERP_API_KEY: Your SerpAPI key for flight data



## 📚 API Endpoints


GET /: Serves the main application page


POST /generate-plan: Generates a travel plan based on provided parameters


POST /chat: Answers questions about the generated travel plan


GET /static/*: Serves static files (images, CSS, JavaScript)



## 🔧 Directory Structure
Include directory structure here if needed

## 🚨 Security Note
This application includes API keys in the environment variables. In a production environment, consider using a more secure method for managing secrets such as Docker secrets, Kubernetes secrets, or a dedicated secrets management service.

## 🌍 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](https://chatgpt.com/c/LICENSE) file for details.

## ✨ Acknowledgements


Groq for providing the LLaMA 3 model API


SerpAPI for Google Flights data


FastAPI framework


Marked.js for Markdown parsing


All other open source libraries used in this project


Created with ❤️ by Abhinav Awasthi
