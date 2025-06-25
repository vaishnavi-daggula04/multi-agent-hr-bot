# app.py
# Force spaCy model download before anything else
import subprocess
import spacy

try:
    spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])


import streamlit as st
from agents import intake_agent, shortlister_agent
from agents import ethics_agent
from agents import evaluator_agent
from agents import report_agent
from agents import interviewer_agent


# Set Streamlit page title
st.set_page_config(page_title="Multi-Agent HR Bot")

st.title("🤖 Multi-Agent Job Candidate Selector")
st.subheader("Step 1: Upload Resume and Job Description")

# Upload resume file
resume_file = st.file_uploader("Upload Resume (PDF format)", type=["pdf"])

# Paste job description
job_description = st.text_area("Paste the Job Description here")

# Only run when both resume and JD are provided
if resume_file and job_description:
    # Save resume to folder
    file_path = intake_agent.save_resume(resume_file)

    # Extract text from resume PDF
    resume_text = intake_agent.extract_text_from_pdf(file_path)

    # Show preview of resume
    st.subheader("📄 Resume Text Preview")
    st.text(resume_text[:500])  # First 500 characters

    # ------------------------
    # Shortlisting Agent Logic
    # ------------------------
    st.subheader("🔍 Resume vs Job Description Matching")

    # Compare resume and JD
    result = shortlister_agent.compare_resume_to_jd(resume_text, job_description)

    # Match score
    st.write(f"✅ **Match Score**: {result['match_score'] * 100}%")

    # Show matched skills
    with st.expander("✅ Matched Keywords"):
        st.write(", ".join(result['matched_keywords']))

    # Show missing skills
    with st.expander("❌ Missing Keywords"):
        st.write(", ".join(result['missing_keywords']))
    # ------------------------
    # Ethics Agent
    # ------------------------
    st.subheader("😇 Ethics Audit")

    candidate_name = st.text_input("Enter Candidate Full Name")

    if candidate_name:
        ethics_result = ethics_agent.ethics_check(candidate_name, resume_text)

        st.write(f"🧠 Inferred Gender: `{ethics_result['inferred_gender']}`")
        st.write(f"📆 Gap Years Detected: `{ethics_result['gap_year_flagged']}`")
        st.write(f"🧮 Fairness Score: `{ethics_result['fairness_score']}`")

        with st.expander("⚠️ Ethics Flags"):
            st.json(ethics_result["ethics_flags"])
    # ------------------------
    # Final Evaluator Agent
    # ------------------------
    st.subheader("🧮 Final Evaluation & Recommendation")

    if candidate_name:
        evaluation_result = evaluator_agent.evaluate_candidate(
            result['match_score'],
            ethics_result['fairness_score'],
            ethics_result['ethics_flags'],
            result['missing_keywords']
        )

        st.write(f"📊 **Final Score:** {evaluation_result['final_score']}")
        st.write(f"📢 **Decision:** {evaluation_result['decision']}")

        with st.expander("💡 Why this decision?"):
            for reason in evaluation_result['explanation']:
                st.markdown(f"- {reason}")

        if st.button("📥 Download Evaluation Report"):
            report_path = report_agent.generate_report(
                candidate_name,
                result['match_score'],
                ethics_result['fairness_score'],
                evaluation_result['decision'],
                evaluation_result['explanation']
            )
            with open(report_path, "rb") as f:
                st.download_button(
                    label="📄 Download PDF",
                    data=f,
                    file_name=report_path,
                    mime="application/pdf"
                )
    # ------------------------
    # Interview Agent
    # ------------------------
    st.subheader("🗣️ Interview Simulation")

    questions = interviewer_agent.get_questions()
    answer_scores = {}

    for i, question in enumerate(questions):
        st.markdown(f"**Q{i+1}: {question}**")
        answer = st.text_area(f"Your Answer to Q{i+1}", key=f"q{i+1}")
        if answer:
            feedback = interviewer_agent.evaluate_answer(answer)
            st.markdown(f"🧠 Feedback: _{feedback}_")
            answer_scores[question] = {"answer": answer, "feedback": feedback}
    # ------------------------
    # Final Verdict Summary
    # ------------------------
    st.markdown("## 🏁 Final Verdict")

    if evaluation_result['decision'] == "✅ Shortlist":
        st.success(f"🎉 Congratulations, {candidate_name}! You have been **selected** for the job based on your strong match and fair evaluation.")
    elif evaluation_result['decision'] == "🟡 Review Manually":
        st.warning(f"⚠️ {candidate_name}, your profile shows potential but needs a **manual review**. Missing skills or gaps were detected.")
    else:
        st.error(f"❌ {candidate_name}, thank you for applying. You were **not selected** due to low alignment with the job requirements.")

