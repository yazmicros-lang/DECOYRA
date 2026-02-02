# 🕵️ DECOYRA — Deceptive Honeypot API for Credential & Brute-Force Attack Detection  

## AI Impact Summit – Buildathon Project

---

## 🚀 Project Overview

**DECOYRA** is a **deceptive API honeypot** built using **FastAPI**, designed to intentionally attract and log malicious activity such as:

- Unauthorized API key usage  
- Credential stuffing attempts  
- Brute-force login attacks  

Instead of blocking attackers outright, DECOYRA **silently observes and records attacker behavior**, creating high-quality datasets that can later power **AI/ML-based cybersecurity systems**.

---

## 🌐 Live Deployment (Important for Judges)

The application is deployed on **Render**.

⚠️ **Note:** This is a backend API (no frontend UI).  
The base URL may show *“Not Found”*, which is expected behavior.

### ✅ Please use the Swagger Docs to test the API:
```
https://decoyra.onrender.com/docs
```

---

## 🎯 Problem Statement

Traditional security systems focus only on **blocking attacks**, but they often fail to **learn from attackers**.

> What if we intentionally expose realistic-looking endpoints to observe how attackers behave?

---

## 🧠 Solution Approach

DECOYRA exposes **fake-but-realistic endpoints** that appear valuable to attackers:

- API key validation endpoint  
- Login, admin, and banking authentication endpoints  

All interactions are logged and analyzed for attack patterns.

---

## 🧩 Architecture Overview

Client / Attacker  
↓  
FastAPI Honeypot Service (DECOYRA)  
↓  
Logging Layer (`attacks.log`)  
↓  
Analytics Endpoint (`/stats`)

---

## 🔐 Key Features

### 1️⃣ API Key Honeypot
- Endpoint: `/honeypot`
- Logs both authorized and unauthorized API key attempts

### 2️⃣ Fake Login Traps
- `/login`
- `/admin/login`
- `/bank/login`

### 3️⃣ Brute-Force Detection
- Detects repeated login attempts
- Logs brute-force alerts

### 4️⃣ Attack Analytics
- Endpoint: `/stats`
- Aggregated attack insights

---

## ⚙️ Tech Stack

- Python 3
- FastAPI
- Uvicorn
- Render Cloud

---

## ▶️ How to Run Locally

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

---

## 🛡️ Ethics

No real data. No real authentication. Research-only defensive security project.

---

👨‍💻 Built for **AI Impact Summit – Buildathon**
