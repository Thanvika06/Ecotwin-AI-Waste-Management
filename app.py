"""
Flask REST API and Single-Page Web Dashboard for:
1. Computer Vision Waste Identification & Classification
2. Digital Twin of the Waste Management Ecosystem
3. Generative AI Operational Recommendations & Copilot
"""

import os
import time
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from config import Config
from cv_engine import vision_classifier, get_all_samples, get_sample_by_id, ConveyorStreamSimulator
from digital_twin import ecosystem_twin, sim_engine, generate_analytics_report
from genai_engine import copilot_engine

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

conveyor_sim = ConveyorStreamSimulator()

@app.route("/")
def index():
    """Serves the problem statement and platform presentation website."""
    return render_template("landing.html", config=Config)

@app.route("/dashboard")
def dashboard():
    """Serves the full operational command center dashboard."""
    return render_template("index.html", config=Config)

# ==========================================
# 1. Computer Vision Endpoints
# ==========================================

@app.route("/api/cv/gallery", methods=["GET"])
def get_sample_gallery():
    """Returns curated gallery of waste items for 1-click CV testing."""
    samples = get_all_samples()
    return jsonify({"success": True, "samples": samples})

@app.route("/api/cv/sample/<sample_id>", methods=["GET"])
def get_single_sample(sample_id):
    """Retrieve details for a single sample item."""
    sample = get_sample_by_id(sample_id)
    if not sample:
        return jsonify({"success": False, "error": "Sample not found"}), 404
    return jsonify({"success": True, "sample": sample})

@app.route("/api/cv/classify", methods=["POST"])
def classify_waste_image():
    """
    Accepts base64 image and optional client-extracted canvas features.
    Runs Computer Vision classification & localization.
    """
    data = request.get_json(silent=True) or {}
    image_data = data.get("image")
    features = data.get("features", {})
    
    if not image_data:
        return jsonify({"success": False, "error": "No image data provided"}), 400
        
    try:
        result = vision_classifier.classify_image(image_data, features)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/cv/conveyor/step", methods=["GET"])
def get_conveyor_stream_item():
    """Simulates real-time MRF conveyor line optical sorting scan."""
    item = conveyor_sim.get_next_stream_item()
    return jsonify({
        "success": True,
        "item": item,
        "total_items_scanned": conveyor_sim.item_count,
        "total_weight_kg": round(conveyor_sim.diverted_weight_grams / 1000.0, 2),
        "contaminants_ejected": conveyor_sim.contaminants_intercepted
    })

# ==========================================
# 2. Digital Twin Ecosystem Endpoints
# ==========================================

@app.route("/api/twin/state", methods=["GET"])
def get_digital_twin_state():
    """Returns real-time snapshot of the digital twin ecosystem."""
    return jsonify({"success": True, "state": ecosystem_twin.get_snapshot()})

@app.route("/api/twin/step", methods=["POST"])
def step_simulation():
    """Advance simulation by N seconds."""
    data = request.get_json(silent=True) or {}
    delta = data.get("delta_seconds", Config.SIM_TIME_STEP_SECONDS)
    state = sim_engine.step(delta)
    return jsonify({"success": True, "state": state})

@app.route("/api/twin/speed", methods=["POST"])
def set_sim_speed():
    """Adjust simulation speed multiplier."""
    data = request.get_json(silent=True) or {}
    speed = data.get("speed", 1.0)
    current_speed = sim_engine.set_speed(speed)
    return jsonify({"success": True, "speed": current_speed})

@app.route("/api/twin/scenario", methods=["POST"])
def inject_sim_scenario():
    """Inject scenario: 'Morning Rush Hour', 'Festival Surge', 'Heavy Rain Contamination Event', 'Reset to Normal'."""
    data = request.get_json(silent=True) or {}
    scenario = data.get("scenario", "Morning Rush Hour")
    state = sim_engine.inject_scenario(scenario)
    return jsonify({"success": True, "state": state})

@app.route("/api/twin/dispatch", methods=["POST"])
def dispatch_truck():
    """Dispatches a truck along an optimized route."""
    data = request.get_json(silent=True) or {}
    truck_id = data.get("truck_id", "TRUCK-01")
    bin_ids = data.get("bin_ids")
    res = sim_engine.dispatch_truck_to_route(truck_id, bin_ids)
    return jsonify(res)

@app.route("/api/twin/reset", methods=["POST"])
def reset_twin():
    """Resets digital twin to initial state."""
    ecosystem_twin.reset()
    return jsonify({"success": True, "state": ecosystem_twin.get_snapshot()})

@app.route("/api/analytics", methods=["GET"])
def get_analytics():
    """Returns aggregated ecosystem analytics and predictive overflow risk."""
    report = generate_analytics_report(ecosystem_twin)
    return jsonify({"success": True, "analytics": report})

# ==========================================
# 3. Generative AI Endpoints
# ==========================================

@app.route("/api/ai/recommendations", methods=["GET"])
def get_ai_recommendations():
    """Generates the 4 strategic AI recommendation packages."""
    snapshot = ecosystem_twin.get_snapshot()
    recs = copilot_engine.generate_recommendations(snapshot)
    return jsonify({"success": True, "recommendations": recs})

@app.route("/api/ai/chat", methods=["POST"])
def copilot_chat():
    """Interactive conversational agent grounded in digital twin state."""
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    history = data.get("history", [])
    
    if not message:
        return jsonify({"success": False, "error": "Message cannot be empty"}), 400
        
    snapshot = ecosystem_twin.get_snapshot()
    res = copilot_engine.chat(message, history, snapshot)
    return jsonify({"success": True, **res})

@app.route("/api/ai/set-key", methods=["POST"])
def set_api_key():
    """Dynamically set Gemini API key."""
    data = request.get_json(silent=True) or {}
    key = data.get("api_key", "").strip()
    
    if not key:
        return jsonify({"success": False, "error": "API key cannot be empty"}), 400
        
    copilot_engine.set_api_key(key)
    vision_classifier.set_api_key(key)
    
    return jsonify({
        "success": True,
        "message": "Gemini API key configured successfully.",
        "copilot_ready": copilot_engine.ready,
        "vision_ready": vision_classifier.gemini_ready
    })

if __name__ == "__main__":
    print(f"Starting {Config.PROJECT_NAME} on http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
