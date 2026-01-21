AI Dashboard Generator
Features : 
-> Accepts JSON data as input
->Accepts natural language prompts for styling and layout
->Uses an LLM (Groq) to generate dashboard HTML/CSS
->Displays dashboards instantly in a Streamlit web app
->Includes validation, safety checks, and retry logic to avoid malformed outputs
->Clean, modern, and colorful UI

How It Works

1.Input
User pastes a JSON object
User provides a text prompt describing dashboard style

2.Processing
Backend validates JSON
Numerical calculations (like totals) are handled in Python
JSON + prompt are sent to an AI model with strict system instructions
3.Output
AI returns static HTML/CSS
The dashboard is rendered directly inside the Streamlit app

Tech Stack :
-Frontend & UI: Streamlit
-Backend Logic: Python
-AI Model API: Groq
-Model Used: llama-3.1-8b-instant
-Environment Management: python-dotenv

Installation & Running Locally : 

1.Clone the repository
git clone https://github.com/Anigeth-02/ai-dashboard-generator.git
cd ai-dashboard-generator

2.Create and activate virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

3.Install dependencies
pip install -r requirements.txt

4.Add API Key
GROQ_API_KEY=your_groq_api_key_here

5.Run the application
python -m streamlit run app_streamlit.py

Deployment : 

1.Push code to GitHub
2.Connect repository on Streamlit Cloud
3.Set app_streamlit.py as the main file
4.Add GROQ_API_KEY in Streamlit Secrets
5.Deploy

Security :
->API keys are not hardcoded
->Secrets are managed using environment variables or Streamlit Secrets
->.env is excluded via .gitignore
