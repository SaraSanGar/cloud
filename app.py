from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import datetime
import os

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)


app = Flask(__name__)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class StressLog(Base):
    __tablename__ = 'stress_log'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    HR = Column(Float)
    EDA = Column(Float)
    TEMP = Column(Float)

Base.metadata.create_all(bind=engine)

@app.route("/")
def home():
    return "✅ Flask conectado a PostgreSQL"

@app.route("/api/save", methods=["POST"])
def save():
    data = request.json
    if not data:
        return jsonify({"error": "Faltan datos"}), 400

    try:

        ts = datetime.datetime.fromtimestamp(data["timestamp"])
        entry = StressLog(
            timestamp=ts,
            HR=data["HR"],
            EDA=data["EDA"],
            TEMP=data["TEMP"]
        )

        db = SessionLocal()
        db.add(entry)
        db.commit()
        db.close()

        return jsonify({"ok": True}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

