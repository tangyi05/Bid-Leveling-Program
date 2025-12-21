"""
Generate Sample Bid PDFs for Testing
This script creates realistic sample construction bid PDFs for testing the Bid Leveling AI system.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
import os

def create_sample_bid(filename, bidder_name, total_cost, labor_cost, material_cost, 
                      equipment_cost, overhead_cost, timeline, qualifications):
    """Create a sample construction bid PDF"""
    
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a4d8f'),
        spaceAfter=30,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#0064ff'),
        spaceAfter=12,
    )
    
    # Title
    story.append(Paragraph(f"CONSTRUCTION BID PROPOSAL", title_style))
    story.append(Paragraph(f"Submitted by: {bidder_name}", styles['Normal']))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    
    # Project Overview
    story.append(Paragraph("PROJECT OVERVIEW", heading_style))
    story.append(Paragraph(
        "We are pleased to submit our bid for the construction of the Commercial Office Building "
        "project located at 123 Main Street. This proposal outlines our complete cost breakdown, "
        "timeline, and qualifications for this project.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.3*inch))
    
    # Cost Breakdown
    story.append(Paragraph("COST BREAKDOWN", heading_style))
    
    cost_data = [
        ['Category', 'Amount', 'Percentage'],
        ['Labor', f'${labor_cost:,}', f'{(labor_cost/total_cost*100):.1f}%'],
        ['Materials', f'${material_cost:,}', f'{(material_cost/total_cost*100):.1f}%'],
        ['Equipment', f'${equipment_cost:,}', f'{(equipment_cost/total_cost*100):.1f}%'],
        ['Overhead & Profit', f'${overhead_cost:,}', f'{(overhead_cost/total_cost*100):.1f}%'],
        ['TOTAL BID', f'${total_cost:,}', '100%'],
    ]
    
    cost_table = Table(cost_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    cost_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a4d8f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e6f2ff')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(cost_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Timeline
    story.append(Paragraph("PROJECT TIMELINE", heading_style))
    story.append(Paragraph(f"Estimated completion time: {timeline}", styles['Normal']))
    story.append(Paragraph(
        "Our timeline includes all phases: site preparation, foundation work, structural "
        "construction, MEP installation, interior finishing, and final inspections.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.3*inch))
    
    # Qualifications
    story.append(Paragraph("COMPANY QUALIFICATIONS", heading_style))
    for qual in qualifications:
        story.append(Paragraph(f"• {qual}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Terms and Conditions
    story.append(Paragraph("TERMS AND CONDITIONS", heading_style))
    story.append(Paragraph(
        "This bid is valid for 60 days from the date of submission. Payment terms are net 30 days. "
        "We maintain comprehensive insurance coverage including general liability and workers' compensation. "
        "All work will be performed in accordance with local building codes and industry standards.",
        styles['Normal']
    ))
    
    # Build PDF
    doc.build(story)
    print(f"✓ Created: {filename}")

def main():
    """Generate sample bid PDFs"""
    
    # Create samples directory
    os.makedirs('sample_bids', exist_ok=True)
    
    print("\n🏗️  Generating Sample Construction Bids...\n")
    
    # Bid 1: Competitive, well-balanced
    create_sample_bid(
        filename='sample_bids/acme_construction_bid.pdf',
        bidder_name='Acme Construction Co.',
        total_cost=2850000,
        labor_cost=1200000,
        material_cost=950000,
        equipment_cost=425000,
        overhead_cost=275000,
        timeline='18 months',
        qualifications=[
            'Licensed General Contractor (License #12345)',
            '25+ years of experience in commercial construction',
            'Completed 50+ similar office building projects',
            'OSHA certified safety program',
            'Strong local supplier relationships',
            'Award-winning quality and safety record'
        ]
    )
    
    # Bid 2: Lower cost but less experienced
    create_sample_bid(
        filename='sample_bids/budget_builders_bid.pdf',
        bidder_name='Budget Builders LLC',
        total_cost=2450000,
        labor_cost=950000,
        material_cost=900000,
        equipment_cost=400000,
        overhead_cost=200000,
        timeline='16 months',
        qualifications=[
            'Licensed General Contractor (License #67890)',
            '10 years of experience',
            'Competitive pricing through efficient processes',
            'Growing portfolio of commercial projects',
            'Strong subcontractor network',
            'Focus on cost-effective solutions'
        ]
    )
    
    # Bid 3: Premium quality, higher cost
    create_sample_bid(
        filename='sample_bids/premier_construction_bid.pdf',
        bidder_name='Premier Construction Group',
        total_cost=3250000,
        labor_cost=1400000,
        material_cost=1100000,
        equipment_cost=500000,
        overhead_cost=250000,
        timeline='20 months',
        qualifications=[
            'Licensed General Contractor (License #11223)',
            '40+ years of industry leadership',
            'LEED Certified Green Building expertise',
            'Multiple industry awards for excellence',
            'Advanced project management technology',
            'Premium materials and craftsmanship',
            'Extended warranty programs',
            'White-glove client service'
        ]
    )
    
    print("\n✅ Sample bids generated successfully!")
    print("📁 Location: ./sample_bids/")
    print("\nYou can now use these PDFs to test the Bid Leveling AI system.\n")

if __name__ == '__main__':
    # Check if reportlab is installed
    try:
        import reportlab
        main()
    except ImportError:
        print("\n⚠️  Error: reportlab package not installed")
        print("Install it with: pip install reportlab")
        print("Then run this script again.\n")
