from llm import analyze_alert
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS alerts (
            id SERIAL PRIMARY KEY,
            source_ip VARCHAR(50),
            attack_type VARCHAR(100),
            severity VARCHAR(20),
            risk_score INTEGER,
            status VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))
    conn.commit()
@app.get("/")
def home():
    return {
        "project": "CyberFusion",
        "status": "running"
    }

@app.post("/alerts")
def create_alert():

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO alerts
                (source_ip, attack_type, severity, risk_score, status)
                VALUES
                ('192.168.1.10', 'Brute Force', 'High', 85, 'Open')
            """)
        )

        conn.commit()

    return {"message": "Alert inserted"}

@app.get("/alerts")
def get_alerts():

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM alerts")
        )

        alerts = []

        for row in result:
            alerts.append(dict(row._mapping))

    return alerts
@app.get("/analyze/{alert_id}")
def analyze(alert_id: int):

    with engine.connect() as conn:
        result = conn.execute(
            text(
                f"""
                SELECT *
                FROM alerts
                WHERE id={alert_id}
                """
            )
        )

        row = result.fetchone()

    if not row:
        return {"error": "Alert not found"}

    alert = dict(row._mapping)

    analysis = analyze_alert(alert)

    return {
        "alert": alert,
        "analysis": analysis
    }
@app.put("/resolve/{alert_id}")
def resolve_alert(alert_id: int):

    with engine.connect() as conn:
        conn.execute(
            text("""
                UPDATE alerts
                SET status='Resolved'
                WHERE id=:id
            """),
            {"id": alert_id}
        )

        conn.commit()

    return {"message": "Alert resolved"}
