# AI Chat & CV Analyzer Project 🤖💬

[![Live Demo](https://img.shields.io/badge/🌍%20Live%20Demo-Click%20Here-brightgreen?style=for-the-badge)](https://ai-helper-72uy.onrender.com/)

**Status:** Work in Progress 🚧  

![Chat Screenshot](https://github.com/user-attachments/assets/48020e3a-c96a-4fec-90b3-2020085e7848)

---

## Overview

**AI Chat & CV Analyzer Project** is a **full-stack AI assistant platform** that combines two main functionalities:

1. **AI Chat** – Real-time chat powered by **Google Gemini API**, allowing users to converse with an intelligent AI assistant.  
2. **CV Analyzer** – Users can upload their CVs, and the AI provides **concise, actionable feedback** tailored to the specified job title.

The backend is built with **FastAPI** and uses **SQLite3** for persistent storage.  
The frontend is fully **responsive**, styled with **Bootstrap 5**, and ensures seamless use across desktop and mobile devices.

The platform includes a **full authentication system**, ensuring that all data is securely associated with authenticated users.

---

## Features

### Authentication & Authorization
- **User registration and login**
- **JWT-based authentication**
- **Protected routes** (Chat & CV Analyzer require login)
- **Secure password hashing** using Argon2
- **Logout support** with token removal
- Navigation elements are hidden or disabled for unauthenticated users

---

### AI Chat
- **AI-powered chat** using Google Gemini.
- **JWT-protected endpoint** – only authenticated users can send messages.
- **User-based chat history**: every message is linked to the logged-in user.
- **Persistent storage**: messages and replies saved in SQLite3.
- **In-memory caching per user** for faster responses.
- **Multi-language support**: replies match the user’s language.
- **Markdown normalization**: AI responses are cleaned for display.
- **Responsive UI** with real-time message updates.

---

### CV Analyzer
- **JWT-protected CV upload**
- Upload CVs in `.pdf`, `.txt`, or `.docx` formats.
- **Job-specific AI feedback**
- **Actionable suggestions** focused strictly on the uploaded CV.
- **Language-aware feedback** (based on job title language).
- **User-based persistence**:
  - CVs are linked to the authenticated user
  - Original content and AI feedback stored in the database

---

## User-Based Data Model

- Each authenticated user has:
  - Chat history
  - Uploaded CVs
- No anonymous or auto-created users
- All database records are linked via `user_id` from the JWT token
- Data isolation is guaranteed between users

---

## Technology Stack

**Backend:**  
- FastAPI  
- SQLAlchemy (ORM)  
- SQLite3  
- Google Gemini API  
- JWT Authentication  

**Frontend:**  
- HTML & CSS (Bootstrap 5)  
- JavaScript  
- Jinja2 Templates  

**Other Tools:**  
- dotenv for environment variables  
- Static file serving via FastAPI  
- PyPDF2 & python-docx for CV parsing  
- In-memory caching for performance  

---


