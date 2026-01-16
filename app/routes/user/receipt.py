from app import app
from flask import render_template, send_file, abort
from app.decorators import approved_required
from datetime import datetime
from werkzeug.utils import secure_filename
import os, tempfile
import pdfkit

# Define a safe directory for receipts
RECEIPTS_DIR = tempfile.mkdtemp(prefix='flask_banking_receipts_')

@app.route('/download_receipt/<filename>')
@approved_required
def download_receipt(filename):
    """Securely download a receipt file."""
    # Sanitize filename to prevent path traversal
    safe_filename = secure_filename(filename)
    safe_path = os.path.join(RECEIPTS_DIR, safe_filename)
    
    # Verify the file exists and is within the allowed directory
    if not os.path.exists(safe_path):
        abort(404)
    
    # Verify the path is still within RECEIPTS_DIR (prevent traversal)
    if not os.path.realpath(safe_path).startswith(os.path.realpath(RECEIPTS_DIR)):
        abort(403)
    
    return send_file(safe_path, as_attachment=True)


@app.route('/success/<filename>')
@approved_required
def payment(filename):
    return render_template('user/payment.html', filename=filename)


def generate_receipt(receipt_data):
    """Generate a PDF receipt and return the filename."""
    html_template_path = "app/templates/user/receipt_template.html"

    # Read HTML content from the separate file
    with open(html_template_path, "r") as file:
        receipt_content = file.read()

    # Format the HTML content with receipt data
    receipt_content = receipt_content.format(**receipt_data)

    # Generate a unique filename for the receipt using timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f'receipt_{timestamp}.pdf'

    # Save files in the secure directory
    temp_html_path = os.path.join(RECEIPTS_DIR, f"temp_{timestamp}.html")
    pdf_path = os.path.join(RECEIPTS_DIR, filename)

    # save the html content to a temporary file
    with open(temp_html_path, "w") as temp_file:
        temp_file.write(receipt_content)

    pdfkit.from_file(temp_html_path, pdf_path)

    # clean the temp html file
    os.remove(temp_html_path)

    return filename  # Return just the filename, not full path