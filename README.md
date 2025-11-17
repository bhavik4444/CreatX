# 🎉 Rupee Rangers
**A fun finance-learning web app for pre-teens — built with Flask.**

Rupee Rangers teaches kids essential money skills through **games**, **levels**, and a **bright doodle-style interface**.

---

## ⭐ Features
- 🎨 **Kid-friendly UI**
- 👤 **Cartoon avatars**
- 🎮 **Mini-game: Coin Jars**
- ❓ **Quiz levels (1–5)**
- 🔥 **XP, level progression, streaks**
- 📅 **Daily question sets**
- 🔐 **Login / Signup with Flask-Login**
- 🗄️ **SQLite + SQLAlchemy backend**

---

## 🏗️ Tech Stack
**Frontend:** HTML, CSS, JavaScript  
**Backend:** Flask, SQLAlchemy, Flask-Login  
**Database:** SQLite  
**Structure:** Blueprints + App Factory

---

## 📁 Project Structure
\`\`\`
rupee_rangers/
│
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── db.py
│   ├── models.py
│   └── routes/
│       ├── __init__.py
│       ├── auth.py
│       └── game.py
│
├── frontend/
│   ├── templates/
│   └── static/
│
└── requirements.txt
\`\`\`

---

## 🚀 Setup

### 1. Install dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 2. Initialize database
\`\`\`bash
flask --app backend.app:create_app init-db
\`\`\`

### 3. Run the server
\`\`\`bash
flask --app backend.app:create_app run --debug
\`\`\`

Open in browser:  
http://127.0.0.1:5000/

---

## 📚 What Kids Learn
- Budgeting  
- Saving habits  
- Scam safety (OTP, fake prizes, links)  
- Banking basics  
- Government schemes (simplified)

---

## 🎯 Why This Project?
- Perfect for hackathons  
- Easy to demo  
- Shows UI/UX thinking for kids  
- Clean backend architecture  
- Gamified learning experience  

---

## ⭐ Support
If you like this project, give it a **star** ⭐
