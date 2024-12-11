import streamlit as st
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf_report(data, filename):
    try:
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph("Fresh Produce Analysis Report", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 20))  # Add more space after title
        
        # Report generation date
        date_text = Paragraph(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
        elements.append(date_text)
        elements.append(Spacer(1, 12))
        
        # Convert data to table format
        table_data = [["Sl No", "Timestamp", "Produce", "Freshness", "Expected Lifespan (Days)"]]
        for item in data:
            row = [
                str(item["Sl No"]),
                item["Timestamp"].split('T')[0],  # Format timestamp to show only date
                item["Produce"],
                str(item["Freshness"]),
                str(item["Expected Lifespan (Days)"])
            ]
            table_data.append(row)
        
        # Create and style table
        table = Table(table_data, repeatRows=1)  # Repeat header row on each page
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOX', (0, 0), (-1, -1), 2, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
        ]))
        
        elements.append(table)
        doc.build(elements)
        return True
        
    except Exception as e:
        st.error(f"Error generating PDF report: {str(e)}")
        return False
