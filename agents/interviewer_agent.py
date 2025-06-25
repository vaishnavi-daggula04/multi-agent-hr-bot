# agents/interviewer_agent.py

interview_questions = [
    "Tell me about yourself.",
    "What is your experience with Python?",
    "How do you handle tight deadlines?",
    "Explain a recent project you worked on.",
    "What are your strengths and weaknesses?"
]

def get_questions():
    return interview_questions

def evaluate_answer(answer):
    if len(answer.split()) < 5:
        return "Too short — please elaborate."
    elif len(answer.split()) < 20:
        return "Fair answer, could be more detailed."
    else:
        return "Good, detailed response!"
