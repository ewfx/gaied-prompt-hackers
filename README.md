# 🚀 Email Classification System

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)


## 🎯 Introduction
This project is an **AI-powered email classification system** that helps automate the categorization of emails based on predefined rules. It utilizes **FastAPI** as the backend and integrates an **LLM (Large Language Model)** to classify emails into structured types.

The project aims to **simplify email processing** by automating classification, making it easier for organizations to handle large volumes of incoming messages efficiently.

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](#)

## 💡 Inspiration
Manually sorting and responding to emails is **time-consuming** and inefficient, especially in organizations that receive thousands of emails daily. Our goal was to build an AI-powered **email classification tool** that can analyze emails and categorize them based on **business rules** while being **easy to deploy and scale**.

## ⚙️ What It Does
- **Extracts email content** (subject, body, attachments) from `.eml` files.
- **Processes rules provided by the user** to classify emails.
- **Uses an LLM (Large Language Model)** to categorize emails into request types.
- **Stores classification results** for easy retrieval.
- **FastAPI backend** to manage API requests.

## 🛠️ How We Built It
- **FastAPI** for backend development.
- **LLM (via API or local model)** for classification.
- **Python's email package** for `.eml` parsing.
- **Database (PostgreSQL / JSON storage)** for rules & classification storage.(Future Work)

## 🚧 Challenges We Faced
- **Generating a realistic email dataset** since no sample data was provided.
- **Designing effective LLM prompts** for classification accuracy.
- **Deciding between a single agent vs multiple agents** for handling classification logic.
- **Optimizing the email extraction and preprocessing pipeline.**


## 🏗️ Tech Stack
- 🔹 **Backend**: FastAPI (Python)
- 🔹 **Frontend**: React (Material-UI)
- 🔹 **AI Model**: Google Gemini

Let us know if you have any questions or need any modifications!

