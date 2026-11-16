"""
Configuration settings for Smart Waste Computer Vision & Digital Twin Ecosystem.
"""
import os

class Config:
    PROJECT_NAME = "EcoTwin - Smart Waste Vision & Digital Twin Ecosystem"
    VERSION = "2.0.0"
    HOST = os.environ.get("HOST", "127.0.0.1")
    PORT = int(os.environ.get("PORT", 5000))
    DEBUG = False
    
    # Generative AI Key (optional, can be passed via env or UI)
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    DEFAULT_GEMINI_MODEL = "gemini-1.5-flash"
    
    # Simulation defaults
    SIM_TIME_STEP_SECONDS = 15  # Each simulation tick = 15 simulated seconds
    BASE_SPEED_MULTIPLIER = 1.0
    
    # Bin alert thresholds
    BIN_WARNING_THRESHOLD_PCT = 70.0
    BIN_CRITICAL_THRESHOLD_PCT = 85.0
    BIN_CONTAMINATION_ALERT_PCT = 25.0
    
    # Carbon mitigation factors (kg CO2e saved per kg diverted vs landfilling)
    CARBON_FACTORS = {
        "Plastics": 1.45,
        "Paper & Cardboard": 0.95,
        "Metals": 4.20,
        "Glass": 0.35,
        "Organics": 0.75,
        "E-Waste": 8.50,
        "Hazardous": 3.10,
        "Landfill / Residual": 0.00
    }
    
    # Commodity market value ($ per metric ton of sorted clean material)
    COMMODITY_PRICES = {
        "Plastics": 380.0,       # rPET / rHDPE clean flakes
        "Paper & Cardboard": 140.0, # Clean OCC / de-inked pulp
        "Metals": 1250.0,        # Sorted aluminum / tin scrap
        "Glass": 65.0,           # Sorted clean cullet
        "Organics": 45.0,        # Premium compost / soil conditioner
        "E-Waste": 3200.0,       # Circuit boards & precious metal extraction
        "Hazardous": -150.0,     # Safe treatment & disposal cost
        "Landfill / Residual": -95.0 # Tipping fee penalty per ton
    }
