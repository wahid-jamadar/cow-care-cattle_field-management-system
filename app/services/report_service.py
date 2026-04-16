from io import BytesIO, StringIO
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from flask import Response
from app.models.health_data import HealthData

def build_csv_response():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Cattle ID", "Temp", "Heart Rate", "SpO2", "Motion", "Timestamp"])

    rows = HealthData.query.order_by(HealthData.timestamp.desc()).all()
    for r in rows:
        writer.writerow([r.id, r.cattle_id, r.temp, r.heart_rate, r.spo2, r.motion, r.timestamp])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=health_report.csv"}
    )

def build_pdf_response():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, height - 40, "Cattle Health Monitoring Report")

    c.setFont("Helvetica", 10)
    y = height - 70
    rows = HealthData.query.order_by(HealthData.timestamp.desc()).limit(25).all()

    for r in rows:
        line = f"Cattle {r.cattle_id} | Temp: {r.temp} | HR: {r.heart_rate} | SpO2: {r.spo2} | Motion: {r.motion} | {r.timestamp}"
        c.drawString(40, y, line[:110])
        y -= 18
        if y < 50:
            c.showPage()
            y = height - 40
            c.setFont("Helvetica", 10)

    c.save()
    buffer.seek(0)

    return Response(
        buffer.getvalue(),
        mimetype="application/pdf",
        headers={"Content-Disposition": "attachment; filename=health_report.pdf"}
    )