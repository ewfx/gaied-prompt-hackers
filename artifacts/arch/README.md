# 📌 Architecture Overview

## 🏗️ System Components

### FastAPI Backend
- Orchestrates everything (API calls, preprocessing, storing results).
- Handles email ingestion, parsing, and classification requests.

### LLM Classification
- Processes emails based on predefined rules.
- Classifies emails into relevant categories.
- Extracts key details such as request type and sub-type.

### Storage
- Stores user-defined classification rules.
- Maintains classification results for emails.

### Frontend 
- React based UI for uploading emails.
- Displays classified results in an easy-to-read format.

---

## 🛠 Components & Their Responsibilities

### 🎛️ User Interface (Optional)
- Upload `.eml` files.
- View classified emails in a structured manner.

### 🚀 FastAPI Backend (Orchestrator)
- Receives and processes emails.
- Extracts email content (subject, body, attachments).
- Fetches stored classification rules.
- Calls the LLM for email classification.
- Stores and returns classification results.

### 🤖 LLM (API-based or Local Model)
- Classifies emails according to predefined rules.
- Extracts structured information such as:
  - Request type
  - Sub-type
  - Key details

### 🗄️ Database / JSON Storage (Future Work)
- Stores classification rules for the system.
- Maintains processed email classifications for retrieval.

---

## 📊 System Flow Diagram (Mermaid)
```mermaid
graph TD;
    A[User Uploads .eml File] -->|Contains Attachments?| B{Yes/No};
    B -- No --> C[Parse Email Content];
    B -- Yes --> D[Use OCR to Extract Text from Attachments];
    D --> C;
    
    C --> E[Collect Parsed Input + Rules];
    E --> F[Call LLM API with Structured Prompt];
    
    F --> G[Store Request & Response in Database];
    G --> H[Send Response to User];
    
    subgraph Processing
        C
        D
        E
        F
    end
    
    subgraph Storage
        G
    end

```

---

🔧 This architecture provides a scalable and flexible foundation for email classification using Gen AI.

# 📌 Project: AI-Powered Email Classification System

## 📂 Project Structure

```

```

## 📌 Responsibilities & Workflow

1. **User Uploads Email (.eml) File** (May contain attachments)
2. **Parse Input:** Extract email body & use OCR for attachments (if needed)
3. **Apply Rules:** Collect parsed content + predefined rules
4. **LLM Classification:** Send structured prompt to LLM for classification
5. **Store & Respond:** Store the request & response (using in-memory storage) and return results

## 📌 Tech Stack

- **Backend:** FastAPI (Async APIs)
- **Storage:** In-memory dictionary (for now, DB integration later)
- **Processing:** OCR for attachments, LLM API for classification
- **Frontend:** Simple Dashboard with results display

## 📌 API Endpoints

1. **POST /upload-rules** → Upload a text file with classification rules
2. **POST /upload-email** → Upload an `.eml` file for processing

## 📌 Next Steps
- Persistent storage for past results
- Improve the LLM classification by using agentic architecture


