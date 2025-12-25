import joblib
from pathlib import Path
import numpy as np
from datetime import datetime
from src.inference.utils import generate_ticket_id
import os
import sqlite3

# paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_DIR = BASE_DIR / "models"
DB_PATH = "/home/ubuntu/ticketing_app/data/tickets.db"

# load artifacts
tfidf = joblib.load(MODEL_DIR / "tfidf_vectorizer_new2.pkl")
model = joblib.load(MODEL_DIR / "logistic_regression_model_new2.pkl")

ROUTING_MAP = {
    "Billing": "Finance Department",
    "Technical Support": "Tech Support Team",
    "Product Issue": "Product Team",
    "Account Management": "Account Services",
    "Other": "Manual Review Queue"
}

def predict_and_route(cleaned_text, complaint_text):
    """
    Predict complaint category and route ticket
    """
    # vectorize
    X_vec = tfidf.transform([cleaned_text])    

    # confidence
    proba = model.predict_proba(X_vec)[0]
    max_confidence = np.max(proba)

    # predict
    predicted_class = model.classes_[np.argmax(proba)]

    # Confidence-based override
    if max_confidence < 0.244:
        return None  # invalid complaint

    elif max_confidence < 0.4:
        predicted_class = "Other"

    # status logic (FINAL & CENTRALIZED)
    if predicted_class == "Other":
        status = "Pending Review"
    else:
        status = "Assigned"


    # routing
    routed_to = ROUTING_MAP.get(predicted_class, "Manual Review Queue")
    conn = sqlite3.connect(DB_PATH)

    return {
        "ticket_id": generate_ticket_id(conn),
        "complaint_text": complaint_text,
        "predicted_category": predicted_class,
        "confidence": round(float(max_confidence), 3),
        "routed_to": routed_to,
        "status": status,
        "created_at": datetime.now().strftime("%y-%m-%d %H:%M:%S")
    }
