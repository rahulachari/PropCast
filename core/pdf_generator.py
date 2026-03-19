from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io


def generate_pdf_report(df, ai_summary, ai_insights, filename):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=5,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#6c757d'),
        spaceAfter=20,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.HexColor('#1a1a2e'),
        spaceBefore=20,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#333333'),
        spaceAfter=8,
        leading=16
    )

    insight_style = ParagraphStyle(
        'InsightStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=8,
        leading=16,
        leftIndent=10
    )

    content = []

    # Header
    content.append(Spacer(1, 20))
    content.append(Paragraph("PROPCAST", title_style))
    content.append(Paragraph("AI Real Estate Market Report", subtitle_style))
    content.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a1a2e')))
    content.append(Spacer(1, 15))

    # Dataset Overview
    content.append(Paragraph("Dataset Overview", heading_style))

    overview_data = [
        ['Property', 'Value'],
        ['File Name', filename],
        ['Total Properties', str(df.shape[0])],
        ['Total Features', str(df.shape[1])],
        ['Missing Values', str(int(df.isnull().sum().sum()))],
    ]

    if 'Price_Lakhs' in df.columns:
        avg = round(df['Price_Lakhs'].mean(), 1)
        avg_crore = round(avg / 100, 2)
        if avg >= 100:
            avg_display = f"Rs {avg_crore} Crore ({int(avg)} Lakhs)"
        else:
            avg_display = f"Rs {int(avg)} Lakhs"
        overview_data.append(['Average Price', avg_display])

        high = df['Price_Lakhs'].max()
        low = df['Price_Lakhs'].min()
        high_display = f"Rs {round(high/100, 2)} Crore" if high >= 100 else f"Rs {int(high)} Lakhs"
        low_display = f"Rs {round(low/100, 2)} Crore" if low >= 100 else f"Rs {int(low)} Lakhs"
        overview_data.append(['Highest Price', high_display])
        overview_data.append(['Lowest Price', low_display])

    if 'Status' in df.columns:
        sold = len(df[df['Status'] == 'Sold'])
        available = len(df[df['Status'] == 'Available'])
        overview_data.append(['Properties Sold', str(sold)])
        overview_data.append(['Properties Available', str(available)])

    overview_table = Table(overview_data, colWidths=[2.5*inch, 4*inch])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    content.append(overview_table)

    # Price by Location
    if 'Location' in df.columns and 'Price_Lakhs' in df.columns:
        content.append(Paragraph("Price by Location", heading_style))

        location_data = [['Location', 'Avg Price', 'Properties']]
        for loc in df['Location'].unique():
            loc_df = df[df['Location'] == loc]
            avg_price = round(loc_df['Price_Lakhs'].mean(), 1)
            count = len(loc_df)
            if avg_price >= 100:
                price_display = f"Rs {round(avg_price/100, 2)} Cr"
            else:
                price_display = f"Rs {int(avg_price)} L"
            location_data.append([loc, price_display, str(count)])

        location_table = Table(location_data, colWidths=[2.5*inch, 2.5*inch, 1.5*inch])
        location_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90d9')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f4ff')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        content.append(location_table)

    # AI Summary
    if ai_summary:
        content.append(Paragraph("AI Market Summary", heading_style))
        content.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#4a90d9')))
        content.append(Spacer(1, 8))
        clean_summary = ai_summary.replace('\n', ' ').strip()
        content.append(Paragraph(clean_summary, body_style))

    # AI Insights
    if ai_insights:
        content.append(Paragraph("AI Hidden Insights", heading_style))
        content.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#4a90d9')))
        content.append(Spacer(1, 8))
        for insight in ai_insights:
            clean_insight = insight.replace('\n', ' ').strip()
            content.append(Paragraph(clean_insight, insight_style))
            content.append(Spacer(1, 5))

    # Footer
    content.append(Spacer(1, 30))
    content.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1a1a2e')))
    content.append(Spacer(1, 8))
    content.append(Paragraph(
        "Generated by PropCast - AI Real Estate Forecasting Platform",
        subtitle_style
    ))

    doc.build(content)
    buffer.seek(0)
    return buffer