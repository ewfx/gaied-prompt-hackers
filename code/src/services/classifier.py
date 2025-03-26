from google import genai
from dotenv import load_dotenv
import os
import base64
from email import message_from_bytes
import pytesseract
from PyPDF2 import PdfReader
from docx import Document

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def extract_text_from_docx(file_path):
    """Extract text from a Word document."""
    text = ""
    try:
        doc = Document(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
    return text

def extract_text_from_image(image_data):
    """Extract text from an image using OCR."""
    try:
        return pytesseract.image_to_string(image_data)
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return ""

def classify_emails(email_messages, classification_rules):
    results = []

    for email_message in email_messages:
        try:
            # Extract email content
            subject = email_message.get('subject', '')
            email_body = ""
            attachments_text = ""

            if email_message.is_multipart():
                for part in email_message.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    
                    # Extract text content
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        email_body = part.get_payload(decode=True).decode()
                    
                    # Process attachments
                    elif "attachment" in content_disposition:
                        file_name = part.get_filename()
                        file_data = part.get_payload(decode=True)
                        
                        # Handle different attachment types
                        if file_name.endswith(".pdf"):
                            with open(file_name, "wb") as f:
                                f.write(file_data)
                            attachments_text += extract_text_from_pdf(file_name)
                        elif file_name.endswith(".docx"):
                            with open(file_name, "wb") as f:
                                f.write(file_data)
                            attachments_text += extract_text_from_docx(file_name)
                        elif content_type.startswith("image/"):
                            attachments_text += extract_text_from_image(file_data)
            else:
                email_body = email_message.get_payload(decode=True).decode()

            # Combine email content and attachments
            email_content = f"Subject: {subject}\n\nEmail Body:\n{email_body}\n\nAttachments:\n{attachments_text}"

            # Prepare Gemini input
            gemini_input = {
                "system_instructions": f"""You are an intelligent AI model designed to classify emails and extract specific information based on predefined request types and sub-request types. Your task is to analyze the provided email content and attachments (if any) and perform the following steps:

                1. **Email Classification:**
                - Identify the primary request type and sub-request type of the email based on the sender's intent.
                - Provide a concise reasoning for your classification, explaining why you chose the identified categories.

                2. **Context-Based Data Extraction:**
                - Based on the identified request type, extract the following configurable fields if present in the email body or attachments:
                    - Deal Name
                    - Amount
                    - Expiration Date
                    - [Add other configurable fields here as needed]
                - If a field is not found, indicate that it's 'Not Found'.

                3. **Duplicate Email Detection:**
                - If the email appears to be a duplicate of a previously processed email (e.g., multiple replies or forwards within a thread), indicate this in the response.

                **Here are the classification rules:**

                {classification_rules}

                **Email Analysis Guidelines:**

                - Carefully read the email subject and body to understand the sender's intent.
                - Analyze any attached documents or images for additional context and information.
                - Prioritize information in the email body over attachments for request type identification.
                - Extract numerical fields (like amount) from attachments if not found in the email body.
                - Provide your response in a structured JSON format as described below.""",
                "email_content": email_content,
                "output_format": {
                    "classification": {
                        "request_type": "[Identified Request Type]",
                        "sub_request_type": "[Identified Sub-Request Type]",
                        "reasoning": "[Reasoning for the classification]"
                    },
                    "extracted_data": {
                        "deal_name": "[Extracted Deal Name or 'Not Found']",
                        "amount": "[Extracted Amount or 'Not Found']",
                        "expiration_date": "[Extracted Expiration Date (YYYY-MM-DD format) or 'Not Found']",
                        "[Other configurable field]": "[Extracted Value or 'Not Found']"
                    },
                    "duplicate_email": "[Yes/No]"
                }
            }

            # Call the Gemini model
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents={"text": str(gemini_input)}
            )

            # Append the result for this email
            results.append({
                "email_subject": subject,
                "status": "Email processed successfully",
                "classification": response.text
            })

        except Exception as e:
            # Append error result for this email
            logging.error(f"Error processing email: {str(e)}", exc_info=True)
            results.append({
                "email_subject": subject,
                "status": "Error processing email",
                "error": str(e)
            })

    return results