from flask import Flask, request, jsonify, send_from_directory
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
CORS(app)  # Enable CORS

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

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
2. **Total Cost**: Extract the total bid amount (if available)
3. **Key Categories**: Break down the bid into main cost categories (e.g., Labor, Materials, Equipment, Subcontractors, Overhead)
4. **Strengths (Pros)**: List 4-6 specific advantages of this bid
5. **Weaknesses (Cons)**: List 4-6 specific concerns or disadvantages
6. **Risk Assessment**: Identify potential risks (LOW/MEDIUM/HIGH)
7. **Pricing Analysis**: Comment on pricing competitiveness and any unusual line items
8. **Recommendation**: Clear recommendation (RECOMMEND/RECOMMEND WITH CAUTION/DO NOT RECOMMEND)
9. **Overall Score**: Rate 1-10

Format your response as JSON with this exact structure:
{{
  "summary": "...",
  "total_cost": "$XXX,XXX or 'Not specified'",
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

def analyze_bid_with_citations(bid_text, bidder_name):
    """Use Claude to analyze construction bid WITH CITATIONS"""

    prompt = f"""You are an expert construction bid analyst. Analyze this construction bid from {bidder_name} and provide a comprehensive evaluation WITH SPECIFIC CITATIONS.

BID DOCUMENT:
{bid_text}

IMPORTANT: For every statement you make, include a direct quote or citation from the original document. When you mention a strength, weakness, or risk, quote the EXACT TEXT from the bid document that supports your analysis.

Please analyze this bid and provide:

1. **Summary**: Brief overview with citations
2. **Total Cost**: Extract the total bid amount (quote exactly)
3. **Key Categories**: Break down with specific quotes
4. **Strengths (Pros)**: List 4-6 advantages, EACH with a direct quote from the document
5. **Weaknesses (Cons)**: List 4-6 concerns, EACH with a direct quote from the document
6. **Risk Assessment**: Identify potential risks with supporting quotes
7. **Pricing Analysis**: Comment with specific numbers from the document
8. **Recommendation**: Clear recommendation with supporting evidence
9. **Overall Score**: Rate 1-10

Format your response as JSON with this exact structure:
{{
  "summary": "...",
  "total_cost": "$XXX,XXX or 'Not specified'",
  "categories": [
    {{"name": "Category Name", "amount": "dollar amount", "citation": "exact quote from document"}}
  ],
  "pros": [
    {{"text": "strength description", "citation": "exact quote from document that supports this"}},
    ...
  ],
  "cons": [
    {{"text": "concern description", "citation": "exact quote from document that supports this"}},
    ...
  ],
  "risks": {{
    "level": "LOW/MEDIUM/HIGH",
    "details": [
      {{"text": "risk description", "citation": "exact quote"}}
    ]
  }},
  "pricing_analysis": "...",
  "recommendation": "RECOMMEND/RECOMMEND WITH CAUTION/DO NOT RECOMMEND",
  "recommendation_rationale": "...",
  "overall_score": 8
}}

CRITICAL: Every pros, cons, and risk item MUST include a "citation" field with the EXACT text from the bid document. If you cannot find a direct quote, use "citation": "Not explicitly stated in document".

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

@app.route('/api/analyze-bid', methods=['POST', 'OPTIONS'])
def analyze_bid():
    """Endpoint to analyze a single bid PDF"""

    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 204

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

@app.route('/api/compare-bids', methods=['POST', 'OPTIONS'])
def compare_bids():
    """Endpoint to compare multiple bids"""

    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 204

    print("=== COMPARE BIDS REQUEST RECEIVED ===")

    if 'files' not in request.files:
        print("ERROR: No files in request")
        return jsonify({"error": "No files uploaded"}), 400

    files = request.files.getlist('files')
    bidder_names = request.form.getlist('bidder_names')

    print(f"Files received: {len(files)}")
    print(f"Bidder names: {bidder_names}")

    if len(files) < 2:
        print("ERROR: Less than 2 files uploaded")
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
        print(f"ERROR: Comparison failed - {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Comparison failed: {str(e)}"}), 500

@app.route('/api/analyze-bid-with-citations', methods=['POST', 'OPTIONS'])
def analyze_bid_with_citations_endpoint():
    """Endpoint to analyze a single bid PDF WITH CITATIONS"""

    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 204

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

        # Analyze with Claude (with citations)
        analysis = analyze_bid_with_citations(bid_text, bidder_name)

        # Add metadata
        analysis['bidder_name'] = bidder_name
        analysis['filename'] = file.filename
        analysis['analyzed_at'] = datetime.now().isoformat()

        return jsonify(analysis)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "bid-analyzer"})

@app.route('/')
def serve_index():
    """Serve the main HTML file"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(base_dir, 'bid-analyzer.html')

@app.route('/bid-compare.html')
def serve_bid_compare():
    """Serve the bid comparison HTML file"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(base_dir, 'bid-compare.html')

@app.route('/bid-analyzer.html')
def serve_bid_analyzer():
    """Serve the bid analyzer HTML file"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(base_dir, 'bid-analyzer.html')

@app.route('/bid-analyzer-enhanced.html')
def serve_bid_analyzer_enhanced():
    """Serve the enhanced bid analyzer HTML file with citations"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(base_dir, 'bid-analyzer-enhanced.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        return send_from_directory(base_dir, path)
    except Exception as e:
        print(f"Error serving {path}: {str(e)}")
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
