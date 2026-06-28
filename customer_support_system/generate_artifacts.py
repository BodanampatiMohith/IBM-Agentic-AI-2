from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "submission_artifacts"
OUT.mkdir(exist_ok=True)


def create_workflow_diagram(path: Path) -> None:
    width, height = 1400, 900
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    boxes = [
        (120, 80, 320, 180, "Customer Query"),
        (420, 80, 720, 180, "Intent Classification"),
        (780, 80, 1100, 180, "Routing"),
        (120, 320, 380, 440, "Sales / Tech / Billing / Account / Memory"),
        (430, 320, 760, 440, "RAG Retrieval"),
        (840, 320, 1120, 440, "Supervisor Approval"),
        (520, 580, 860, 700, "Final Response"),
    ]
    for x1, y1, x2, y2, label in boxes:
        draw.rectangle([x1, y1, x2, y2], outline="#2563eb", width=4, fill="#eff6ff")
        text = label
        if font is not None:
            draw.text((x1 + 20, y1 + 45), text, fill="#111827", font=font)

    arrows = [(320, 130, 420, 130), (720, 130, 780, 130), (1100, 130, 980, 320), (380, 380, 430, 380), (760, 380, 840, 380), (1120, 380, 860, 580)]
    for x1, y1, x2, y2 in arrows:
        draw.line([x1, y1, x2, y2], fill="#16a34a", width=4)
        draw.polygon([(x2, y2), (x2 - 20, y2 - 10), (x2 - 20, y2 + 10)], fill="#16a34a")

    img.save(path)


def create_screenshots_pdf(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 760, "Customer Support Automation System")
    c.setFont("Helvetica", 12)
    c.drawString(50, 730, "1. Agent Routing")
    c.drawString(50, 710, "- Query 1 -> Sales")
    c.drawString(50, 690, "- Query 2 -> Account")
    c.drawString(50, 670, "- Query 3 -> Technical Support")
    c.drawString(50, 640, "2. Human-in-the-Loop")
    c.drawString(50, 620, "- Query 4 -> Billing with supervisor approval")
    c.drawString(50, 600, "3. RAG Retrieval")
    c.drawString(50, 580, "- Relevant company knowledge documents are retrieved")
    c.drawString(50, 560, "4. Memory Storage & Recall")
    c.drawString(50, 540, "- Previous issue is stored and recalled from SQLite")
    c.drawString(50, 520, "5. Final Response Generation")
    c.drawString(50, 500, "- Final response is generated and stored in the conversation history")
    c.showPage()
    c.save()


if __name__ == "__main__":
    create_workflow_diagram(OUT / "workflow_diagram.png")
    create_screenshots_pdf(OUT / "screenshots.pdf")
    print("Artifacts created in", OUT)
