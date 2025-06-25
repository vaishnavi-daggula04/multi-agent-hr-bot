# agents/report_agent.py

from fpdf import FPDF

def remove_emojis(text):
    """Remove emojis and unsupported characters for PDF"""
    return text.encode("ascii", "ignore").decode()

def generate_report(name, match_score, fairness_score, decision, explanation):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Candidate Evaluation Report", ln=True, align="C")
    pdf.ln(10)

    # Clean text inputs to avoid Unicode errors
    clean_name = remove_emojis(name)
    clean_decision = decision.replace("✅", "Shortlist").replace("❌", "Reject").replace("🟡", "Review")
    clean_explanation = [remove_emojis(line) for line in explanation]

    pdf.cell(200, 10, txt=f"Candidate Name: {clean_name}", ln=True)
    pdf.cell(200, 10, txt=f"Match Score: {match_score * 100}%", ln=True)
    pdf.cell(200, 10, txt=f"Fairness Score: {fairness_score}", ln=True)
    pdf.cell(200, 10, txt=f"Final Decision: {clean_decision}", ln=True)
    pdf.ln(10)

    pdf.multi_cell(0, 10, txt="Explanation:\n" + "\n".join(f"- {line}" for line in clean_explanation))

    output_path = f"report_{clean_name.replace(' ', '_')}.pdf"
    pdf.output(output_path)
    return output_path
