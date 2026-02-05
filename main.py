import os
from fastapi import FastAPI, Request, Header, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="DECOYRA",
    description="Agentic Honeypot API for detecting credential abuse and scam activity",
    version="1.0.0"
)

API_KEY = "guvi-secret-key-123"
LOG_FILE = "attacks.log"


# -------------------------
# LOGGING HELPER
# -------------------------
def log_attack(data: str):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(data + "\n")


# -------------------------
# BASIC HEALTH CHECK
# -------------------------
@app.get("/")
def home():
    return {"message": "Service is running"}


# -------------------------
# REQUEST MODELS
# -------------------------
class ScamMessage(BaseModel):
    sessionId: str
    message: dict
    conversationHistory: list = []
    metadata: dict = {}


class LoginAttempt(BaseModel):
    username: str
    password: str


# -------------------------
# SCAM DETECTION / HONEYPOT RESPONSE
# -------------------------
@app.post("/honeypot")
async def honeypot(
    payload: ScamMessage,
    request: Request,
    x_api_key: str = Header(None)
):
    if x_api_key not in ["guvi-secret-key-123", "dev-fallback-key"]:
        raise HTTPException(status_code=401, detail="Invalid API key")

    scam_text = payload.message.get("text", "").lower()

    if "blocked" in scam_text or "suspended" in scam_text:
        reply = "Why is my account being suspended?"
    elif "otp" in scam_text:
        reply = "I did not receive any OTP. Can you resend?"
    elif "verify" in scam_text:
        reply = "How do I verify it?"
    else:
        reply = "Can you explain this again?"

    log_attack(
        f"SCAM MESSAGE | IP={request.client.host} | TEXT={scam_text}"
    )

    return {
        "status": "success",
        "reply": reply
    }


# -------------------------
# LOGIN LOGGER + BRUTE FORCE DETECTION
# -------------------------
def log_login_attempt(endpoint: str, request: Request, creds: LoginAttempt):
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent")
    time = datetime.utcnow()

    log_data = (
        f"[{time}] "
        f"ENDPOINT={endpoint} | "
        f"IP={client_ip} | "
        f"User-Agent={user_agent} | "
        f"USERNAME={creds.username} | "
        f"PASSWORD={creds.password}"
    )

    log_attack("🚨 LOGIN ATTEMPT " + log_data)

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()

        attempts = 0
        alert_already_logged = False

        for line in reversed(lines):
            if f"⚠️ POSSIBLE BRUTE FORCE ATTACK | IP={client_ip}" in line:
                alert_already_logged = True
                break

            if "🚨 LOGIN ATTEMPT" in line and f"IP={client_ip}" in line:
                attempts += 1

        if attempts >= 5 and not alert_already_logged:
            alert = (
                f"[{time}] ⚠️ POSSIBLE BRUTE FORCE ATTACK | "
                f"IP={client_ip} | "
                f"ATTEMPTS={attempts}"
            )
            log_attack(alert)

    except FileNotFoundError:
        pass


# -------------------------
# FAKE LOGIN ENDPOINTS
# -------------------------
@app.post("/login")
async def login(creds: LoginAttempt, request: Request):
    log_login_attempt("/login", request, creds)
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/admin/login")
async def admin_login(creds: LoginAttempt, request: Request):
    log_login_attempt("/admin/login", request, creds)
    raise HTTPException(status_code=401, detail="Invalid admin credentials")


@app.post("/bank/login")
async def bank_login(creds: LoginAttempt, request: Request):
    log_login_attempt("/bank/login", request, creds)
    raise HTTPException(status_code=401, detail="Authentication failed")


# -------------------------
# ATTACK STATISTICS ENDPOINT
# -------------------------
@app.get("/stats")
def get_stats():
    stats = {
        "total_login_attempts": 0,
        "brute_force_alerts": 0,
        "attacks_by_ip": {},
        "attacks_by_endpoint": {}
    }

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            for line in file:
                if "🚨 LOGIN ATTEMPT" in line:
                    stats["total_login_attempts"] += 1

                    if "IP=" in line:
                        ip = line.split("IP=")[1].split(" |")[0]
                        stats["attacks_by_ip"][ip] = (
                            stats["attacks_by_ip"].get(ip, 0) + 1
                        )

                    if "ENDPOINT=" in line:
                        endpoint = line.split("ENDPOINT=")[1].split(" |")[0]
                        stats["attacks_by_endpoint"][endpoint] = (
                            stats["attacks_by_endpoint"].get(endpoint, 0) + 1
                        )

                if "⚠️ POSSIBLE BRUTE FORCE ATTACK" in line:
                    stats["brute_force_alerts"] += 1

    except FileNotFoundError:
        pass

    return stats






