from flask import Flask, render_template, request, jsonify
import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@app.route("/")
def home():
    return render_template("index.html")

SYSTEM_PROMPT = """
You are a frontend UI designer.

STRICT RULES:
- Output ONLY final HTML and CSS
- NO templates, NO variables, NO loops
- Use modern colors and spacing
- Use cards, shadows, and rounded corners
- Use Google Font like 'Poppins' or 'Inter'
- Use soft background colors and accent colors
- DO NOT explain anything
- Output must start with <html> and end with </html>
"""




@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        json_data = json.loads(data["json"])
        user_prompt = data["prompt"]

        full_prompt = f"""
JSON Data:
{json.dumps(json_data, indent=2)}

User Instructions:
{user_prompt}
"""

        response = client.chat.completions.create(
     model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": full_prompt}
    ]
)


        html_output = response.choices[0].message.content.strip()

        # 🔍 DEBUG PRINT (CORRECT PLACE)
        print("AI OUTPUT:\n", html_output)

        # 🧹 Remove markdown code blocks if present
        if html_output.startswith("```"):
            html_output = html_output.replace("```html", "")
            html_output = html_output.replace("```", "").strip()

        return jsonify({"html": html_output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
