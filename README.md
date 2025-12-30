# AI Chat & CV Analyzer Project 🤖💬

[![Live Demo](https://img.shields.io/badge/🌍%20Live%20Demo-Click%20Here-brightgreen?style=for-the-badge)](https://ai-helper-72uy.onrender.com/)

**Status:** Work in Progress 🚧  

![Chat Screenshot](https://github.com/user-attachments/assets/48020e3a-c96a-4fec-90b3-2020085e7848)

---

## Overview

**AI Chat & CV Analyzer Project** is a **full-stack AI assistant platform** that combines two main functionalities:

1. **AI Chat** – Real-time chat powered by **Google Gemini API**, allowing users to converse with an intelligent AI assistant.  
2. **CV Analyzer** – Users can upload their CVs, and the AI provides **concise, actionable feedback** tailored to the specified job title.

The backend is built with **FastAPI** and uses **SQLite3** for persistent storage. The frontend is fully **responsive**, styled with **Bootstrap 5**, and ensures seamless use across desktop and mobile devices.

---

## Features

### AI Chat
- **AI-powered chat**: Interactions handled by Google Gemini's latest model.
- **Multi-language support**: The AI responds in the same language as the user input.
- **Persistent chat history**: All messages stored in SQLite3.
- **In-memory caching**: Frequently asked messages are cached for faster responses.
- **Markdown normalization**: AI replies are stripped of Markdown formatting for clean display.
- **Responsive UI**: Works well on desktop and mobile.
- **Real-time updates**: Messages appear instantly without page reloads.

### CV Analyzer
- **Upload CVs** in `.pdf`, `.txt`, or `.docx` formats.
- **Job-specific feedback**: AI analyzes CV content in the context of the provided job title.
- **Actionable suggestions**: Highlights what to add, remove, or rephrase in each CV section.
- **Language-aware feedback**: Response is in the same language as the job title.
- **Stored in database**: All uploaded CVs and feedback are saved for later reference.

---

## Technology Stack

**Backend:**  
- FastAPI  
- SQLAlchemy (ORM)  
- SQLite3  
- Google Gemini API  

**Frontend:**  
- HTML & CSS (Bootstrap 5)  
- JavaScript (dynamic chat & CV interactions)  
- Jinja2 templates  

**Other Tools:**  
- dotenv for environment variables  
- Static file serving via FastAPI  
- PyPDF2 & python-docx for CV parsing  
- In-memory caching for performance  

---


