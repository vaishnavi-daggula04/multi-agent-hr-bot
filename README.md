# 🤖 Multi-Agent HR Bot

An AI-powered, Streamlit-based job candidate screening tool that simulates an end-to-end hiring process using multiple intelligent agents.

## 🚀 Live Demo

🌐 [Launch the App on Streamlit Cloud](https://<your-streamlit-app-url>)  
📎 [View Project Repository](https://github.com/vaishnavi-daggula04/multi-agent-hr-bot)

> ✅ Upload a resume (PDF), paste a job description, and let the agents do the hiring!

---

## 🧠 Features

| Agent | Role |
|-------|------|
| 📥 **Intake Agent** | Parses and extracts text from uploaded resumes |
| 🔍 **Shortlister Agent** | Compares resume to job description using NLP and keyword analysis |
| 😇 **Ethics Agent** | Detects potential gender bias, employment gaps, and fairness score |
| 🧮 **Evaluator Agent** | Computes final candidate score and decision |
| 💬 **Interview Agent** | Simulates basic interview Q&A with feedback |
| 📝 **Report Generator Agent** | Generates a downloadable PDF evaluation report |

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **Streamlit** – frontend UI
- **spaCy** – NLP engine
- **pdfplumber** – PDF text extraction
- **FPDF** – PDF report generation
- **gender-guesser** – infers gender from name

---

## 📦 Installation

### 1. Clone the repository
git clone https://github.com/vaishnavi-daggula04/multi-agent-hr-bot.git
cd multi-agent-hr-bot

2. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

4. Install dependencies
pip install -r requirements.txt

6. Run the app
streamlit run app.py

📁 Project Structure
bash
Copy
Edit
multi-agent-hr-bot/
│
├── app.py                        # Main Streamlit application
├── requirements.txt              # Required Python packages
├── setup.sh                      # (Optional) spaCy model installer
├── agents/
│   ├── intake_agent.py
│   ├── shortlister_agent.py
│   ├── ethics_agent.py
│   ├── evaluator_agent.py
│   ├── report_agent.py
│   └── interviewer_agent.py

📄 Sample Use Case

Upload resume.pdf

Paste a job description

Get:

Match score

Ethics audit

Interview simulation

Final verdict

Downloadable evaluation PDF
