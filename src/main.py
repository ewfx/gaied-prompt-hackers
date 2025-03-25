from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from services.rule_manager import rule_manager
import uvicorn
import json
import re
from typing import Dict, List

app = FastAPI(title="Email Classification System")

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
    try:
        content = await file.read()
        rules = json.loads(content.decode())
        rule_manager.add_rules(rules)
        global classification_rules
        classification_rules = json.loads(content)
        return JSONResponse({"status": "Rules uploaded successfully"})
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-email")
async def upload_email(file: UploadFile = File(...)):
    try:
        content = await file.read()
        email_text = content.decode()
        categories = rule_manager.classify_email(email_text)
        content_str = content.decode("utf-8").lower()
    
        categories = []
        for category, keywords in classification_rules.items():
            if any(keyword.lower() in content_str for keyword in keywords):
                categories.append(category)
    
        if not categories:
            categories.append("uncategorized")
    
        return JSONResponse({
            "status": "Email processed successfully",
            "categories": categories
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
