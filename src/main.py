from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from services.rule_manager import rule_manager
import uvicorn
import json
import logging
from email import message_from_bytes

app = FastAPI(title="Email Classification System")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Replace "*" with specific origins if needed.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

classification_rules = {}

@app.get("/")
async def root():
    return {
        "message": "Welcome to Email Classification System API",
        "endpoints": {
            "upload_rules": "/upload-rules",
            "upload_email": "/upload-email"
        }
    }

@app.post("/upload-rules")
async def upload_rules(file: UploadFile = File(...)):
    global classification_rules  # Declare as global to modify the variable
    try:
        logging.info("Received file for rules upload.")
        content = await file.read()
        logging.info(f"File content: {content.decode()[:100]}")  # Log first 100 characters of the file
        rules = json.loads(content.decode())
        logging.info(f"Parsed rules: {rules}")
        rule_manager.add_rules(rules)  # Add rules to the RuleManager instance
        classification_rules = rule_manager.get_rules()  # Update the global variable
        logging.info(f"Updated classification rules: {classification_rules}")
        return JSONResponse({"status": "Rules uploaded successfully"})
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        logging.error(f"Error uploading rules: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

logging.basicConfig(level=logging.INFO)

def extract_email_body(email_message):
    email_body = ""
    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            # Get the plain text part of the email
            if content_type == "text/plain" and "attachment" not in content_disposition:
                email_body = part.get_payload(decode=True).decode()
                break

            # Fallback to HTML if plain text is not found
            if content_type == "text/html" and "attachment" not in content_disposition:
                email_body = part.get_payload(decode=True).decode()
    else:
        # For non-multipart emails, get the payload directly
        email_body = email_message.get_payload(decode=True).decode()

    return email_body

@app.post("/upload-email")
async def upload_email(file: UploadFile = File(...)):
    try:
        # Read the uploaded .eml file
        content = await file.read()
        email_message = message_from_bytes(content)
        email_body = extract_email_body(email_message)

        logging.info(f"Extracted email body: {email_body}")

        # Convert the email body to lowercase for case-insensitive matching
        email_body_lower = email_body.lower()

        # Classify the email based on the rules
        categories = []
        for category, keywords in classification_rules.items():
            logging.info(f"Checking category: {category}, keywords: {keywords}")
            if any(keyword.lower() in email_body_lower for keyword in keywords):
                categories.append(category)

        # If no categories match, classify as "uncategorized"
        if not categories:
            categories.append("uncategorized")

        logging.info(f"Email classified into categories: {categories}")

        return JSONResponse({
            "status": "Email processed successfully",
            "categories": categories
        })
    except Exception as e:
        logging.error(f"Error processing email: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the email.")
def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()