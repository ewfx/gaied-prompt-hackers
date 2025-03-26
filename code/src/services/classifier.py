from google import genai
from dotenv import load_dotenv
import os
import base64
from email import message_from_bytes

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def classify_email(email_message, classification_rules):
    """Process email content and prepare input for the Gemini model."""
    
    # Extract email content
    subject = email_message.get('subject', '')
    
    # Get email body
    email_body = ""
    image_attachments = []
    
    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            # Extract text content
            if content_type == "text/plain" and "attachment" not in content_disposition:
                email_body = part.get_payload(decode=True).decode()
            
            # Handle image attachments
            elif content_type.startswith('image/'):
                try:
                    image_data = part.get_payload(decode=True)
                    encoded_image = base64.b64encode(image_data).decode('utf-8')
                    image_attachments.append({
                        "mime_type": content_type,
                        "data": encoded_image
                    })
                except Exception as e:
                    print(f"Error processing image attachment: {e}")
    else:
        email_body = email_message.get_payload(decode=True).decode()

    email_content = f"Subject: {subject}\n\n{email_body}"
    
    # Format classification rules for the prompt
    classification_info = "\n".join([
        f"- {category}: {', '.join(keywords)}"
        for category, keywords in classification_rules.items()
    ])

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

**Predefined Request Types and Sub-Request Types:**

{classification_info}

**Email Analysis Guidelines:**

- Carefully read the email subject and body to understand the sender's intent.
- Analyze any attached documents or images for additional context and information.
- Prioritize information in the email body over attachments for request type identification.
- Extract numerical fields (like amount) from attachments if not found in the email body.
- Provide your response in a structured JSON format as described below.""",
        "email_content": email_content,
        "image_attachments": image_attachments,
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
            }
        }
    }
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro-exp-03-25",
            contents={"text": str(gemini_input)}
        )
        return response.text
    except Exception as e:
        return {"error": f"Classification failed: {str(e)}"}

