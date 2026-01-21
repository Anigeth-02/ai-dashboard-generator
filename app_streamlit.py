import streamlit as st
import json
import os
from groq import Groq
from dotenv import load_dotenv

# --------------------------------------------------
# ENV + CLIENT
# --------------------------------------------------
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="AI Dashboard Generator",
    layout="wide"
)

# --------------------------------------------------
# GLOBAL STYLES
# --------------------------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #eef2ff, #f8fafc);
}
.main {
    background-color: transparent;
}
h1 {
    text-align: center;
    color: #1e293b;
}
.subtitle {
    text-align: center;
    color: #475569;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("<h1>🎨 AI Dashboard Generator</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Convert JSON data into clean, beautiful dashboards using AI</div>",
    unsafe_allow_html=True
)

# --------------------------------------------------
# INPUTS
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    json_input = st.text_area(
        "📥 Paste JSON Data",
        height=260,
        placeholder='{"report_title": "Monthly Office Spending"}'
    )

with col2:
    user_prompt = st.text_area(
        "📝 Describe Dashboard Style",
        height=260,
        placeholder="Create a modern colorful dashboard with cards and tables"
    )

# --------------------------------------------------
# SYSTEM PROMPT (STRICT)
# --------------------------------------------------
SYSTEM_PROMPT = """
You are a frontend UI developer.

ABSOLUTE RULES (NO EXCEPTIONS):
- Output ONLY static, browser-ready HTML and CSS
- DO NOT use PHP, JavaScript templating, or server-side code
- DO NOT use PHP tags (<? ?>), echo, variables, or concatenation
- DO NOT use Jinja, Blade, React, Vue, loops, or placeholders
- ALL values must be written explicitly as plain HTML text
- DO NOT explain anything
- DO NOT use markdown or code fences
- Output must start with <html> and end with </html>

Generate clean, valid HTML that a browser can render directly.
"""

# --------------------------------------------------
# HELPER: OUTPUT VALIDATION
# --------------------------------------------------
def is_invalid_html(output: str) -> bool:
    banned_patterns = ["<?", "?>", "echo", "print", "'.", ".'", "{{", "{%", "%}"]
    return any(p in output for p in banned_patterns)

# --------------------------------------------------
# BUTTON
# --------------------------------------------------
if st.button("🚀 Generate Dashboard", use_container_width=True):
    try:
        # ---------------- JSON VALIDATION ----------------
        data = json.loads(json_input)

        # ---------------- SAFE CALCULATION ----------------
        if "expenses" in data:
            total = sum(item.get("amount", 0) for item in data["expenses"])
            data["total_spending"] = f"{total:.2f}"

        # ---------------- PRIMARY PROMPT ----------------
        base_prompt = f"""
Below is VERIFIED DATA.
You MUST convert it into FINAL STATIC HTML.

DATA:
Title: {data.get("report_title")}
Currency: {data.get("currency")}
Total Spending: {data.get("total_spending")}

Expenses (WRITE EACH ROW MANUALLY, NO LOOPS):
{json.dumps(data.get("expenses", []), indent=2)}

STRICT INSTRUCTIONS:
- Write every table row explicitly
- Use only HTML tags like <div>, <table>, <tr>, <td>, <h1>, <p>
- DO NOT generate PHP, templates, or string concatenation

DESIGN REQUEST:
{user_prompt}
"""

        # ---------------- FIRST AI CALL ----------------
        with st.spinner("✨ Generating dashboard..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": base_prompt}
                ]
            )

        html_output = response.choices[0].message.content.strip()

        # Remove markdown fences if present
        if html_output.startswith("```"):
            html_output = (
                html_output
                .replace("```html", "")
                .replace("```", "")
                .strip()
            )

        # ---------------- AUTO-RETRY ON INVALID OUTPUT ----------------
        if is_invalid_html(html_output):
            correction_prompt = f"""
The previous output was INVALID.

REGENERATE the dashboard as:
- PURE STATIC HTML ONLY
- NO PHP
- NO variables
- NO concatenation
- NO placeholders or symbols like {{ }}, <? ?>

USE THIS DATA EXACTLY:
{json.dumps(data, indent=2)}

Return ONLY clean HTML starting with <html> and ending with </html>.
"""

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": correction_prompt}
                ]
            )

            html_output = response.choices[0].message.content.strip()

            if html_output.startswith("```"):
                html_output = (
                    html_output
                    .replace("```html", "")
                    .replace("```", "")
                    .strip()
                )

            if is_invalid_html(html_output):
                st.error("❌ AI could not generate valid HTML. Please try again.")
                st.stop()

        # ---------------- BEAUTIFUL WRAPPER ----------------
        styled_html = f"""
        <html>
        <head>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
        <style>
        body {{
            background: linear-gradient(135deg, #eef2ff, #f8fafc);
            font-family: 'Poppins', sans-serif;
        }}
        .dashboard-container {{
            max-width: 1000px;
            margin: 30px auto;
            padding: 25px;
            background: white;
            border-radius: 18px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.08);
        }}
        </style>
        </head>
        <body>
            <div class="dashboard-container">
                {html_output}
            </div>
        </body>
        </html>
        """

        st.success("✅ Dashboard generated successfully!")

        st.components.v1.html(
            styled_html,
            height=700,
            scrolling=True
        )

    except json.JSONDecodeError:
        st.error("❌ Invalid JSON format. Please check your input.")

    except Exception as e:
        st.error(str(e))

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center;color:#64748b;'>Built with ❤️ using Streamlit + Groq</div>",
    unsafe_allow_html=True
)
