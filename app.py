from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import pdfplumber
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize Anthropic client
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def analyze_bid_with_claude(bid_text, bidder_name):
    """Use Claude to analyze construction bid"""
    
    prompt = f"""You are an expert construction bid analyst. Analyze this construction bid from {bidder_name} and provide a comprehensive evaluation.

BID DOCUMENT:
{bid_text}

Please analyze this bid and provide:

1. **Summary**: Brief overview of the bid (2-3 sentences)
2. **Key Categories**: Break down the bid into main cost categories (e.g., Labor, Materials, Equipment, Subcontractors, Overhead)
3. **Strengths (Pros)**: List 4-6 specific advantages of this bid
4. **Weaknesses (Cons)**: List 4-6 specific concerns or disadvantages
5. **Risk Assessment**: Identify potential risks (LOW/MEDIUM/HIGH)
6. **Pricing Analysis**: Comment on pricing competitiveness and any unusual line items
7. **Recommendation**: Clear recommendation (RECOMMEND/RECOMMEND WITH CAUTION/DO NOT RECOMMEND)
8. **Overall Score**: Rate 1-10

Format your response as JSON with this exact structure:
{{
  "summary": "...",
  "categories": [
    {{"name": "Category Name", "amount": "dollar amount or description", "percentage": "% of total if available"}}
  ],
  "pros": ["pro 1", "pro 2", ...],
  "cons": ["con 1", "con 2", ...],
  "risks": {{"level": "LOW/MEDIUM/HIGH", "details": ["risk 1", "risk 2", ...]}},
  "pricing_analysis": "...",
  "recommendation": "RECOMMEND/RECOMMEND WITH CAUTION/DO NOT RECOMMEND",
  "recommendation_rationale": "...",
  "overall_score": 8
}}

Respond ONLY with valid JSON, no other text."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Parse Claude's response
    response_text = message.content[0].text
    
    # Clean up response if it has markdown code blocks
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
    
    return json.loads(response_text.strip())

@app.route('/api/analyze-bid', methods=['POST'])
def analyze_bid():
    """Endpoint to analyze a single bid PDF"""
    
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    bidder_name = request.form.get('bidder_name', 'Unknown Bidder')
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400
    
    try:
        # Extract text from PDF
        bid_text = extract_text_from_pdf(file)
        
        if not bid_text.strip():
            return jsonify({"error": "Could not extract text from PDF"}), 400
        
        # Analyze with Claude
        analysis = analyze_bid_with_claude(bid_text, bidder_name)
        
        # Add metadata
        analysis['bidder_name'] = bidder_name
        analysis['filename'] = file.filename
        analysis['analyzed_at'] = datetime.now().isoformat()
        
        return jsonify(analysis)
    
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

@app.route('/api/compare-bids', methods=['POST'])
def compare_bids():
    """Endpoint to compare multiple bids"""
    
    if 'files' not in request.files:
        return jsonify({"error": "No files uploaded"}), 400
    
    files = request.files.getlist('files')
    bidder_names = request.form.getlist('bidder_names')
    
    if len(files) < 2:
        return jsonify({"error": "Please upload at least 2 bids to compare"}), 400
    
    try:
        analyses = []
        
        for i, file in enumerate(files):
            if not file.filename.endswith('.pdf'):
                continue
            
            bidder_name = bidder_names[i] if i < len(bidder_names) else f"Bidder {i+1}"
            
            # Extract and analyze
            bid_text = extract_text_from_pdf(file)
            analysis = analyze_bid_with_claude(bid_text, bidder_name)
            analysis['bidder_name'] = bidder_name
            analysis['filename'] = file.filename
            
            analyses.append(analysis)
        
        # Generate comparison summary with Claude
        comparison_prompt = f"""Compare these {len(analyses)} construction bids and provide a final recommendation.

BIDS ANALYZED:
{json.dumps(analyses, indent=2)}

Provide a comparison summary that includes:
1. **Winner**: Which bid you recommend and why
2. **Key Differentiators**: What sets the bids apart
3. **Cost Comparison**: If pricing info is available
4. **Final Recommendation**: Clear guidance for decision-making

Format as JSON:
{{
  "recommended_bidder": "bidder name",
  "comparison_summary": "...",
  "key_differentiators": ["diff 1", "diff 2", ...],
  "final_recommendation": "..."
}}"""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": comparison_prompt}]
        )
        
        comparison_text = message.content[0].text
        if comparison_text.startswith("```"):
            comparison_text = comparison_text.split("```")[1]
            if comparison_text.startswith("json"):
                comparison_text = comparison_text[4:]
        
        comparison = json.loads(comparison_text.strip())
        
        return jsonify({
            "individual_analyses": analyses,
            "comparison": comparison,
            "analyzed_at": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({"error": f"Comparison failed: {str(e)}"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "bid-analyzer"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
