from fpdf import FPDF
import datetime

def generate_report(solar, wind, load, soc, freq, volt, temp, pred, risk, actions):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 15, "GridGuard - Smart Grid Report", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(0, 10, f"Prediction: {'FAULT' if pred==1 else 'NORMAL'} | Risk: {risk}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Grid Parameters:", ln=True)
    pdf.set_font("Arial", "", 12)
    for label, val in [("Solar", solar), ("Wind", wind), ("Load", load), ("Battery SOC", soc), ("Frequency", freq), ("Voltage", volt), ("Temperature", temp)]:
        pdf.cell(0, 8, f"{label}: {val}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "AI Agent Actions:", ln=True)
    pdf.set_font("Arial", "", 11)
    for a in actions:
        # Remove ALL emoji / special chars - keep only safe ASCII
        clean = "".join(c for c in a if ord(c) < 128)
        clean = clean.strip()
        if not clean:
            clean = "Action taken by AI Agent"
        # Use cell with wrap - split long lines
        pdf.cell(0, 8, f"- {clean[:90]}", ln=True)
        if len(clean) > 90:
            pdf.cell(0, 8, f"  {clean[90:180]}", ln=True)
    return bytes(pdf.output())