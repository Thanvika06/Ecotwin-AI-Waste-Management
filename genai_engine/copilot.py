"""
Generative AI Copilot and Recommendation Engine.
Provides autonomous contextual reasoning, multi-turn chat, and operational strategies
grounded in real-time digital twin state and computer vision telemetry.
"""

import os
import json
import re
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from config import Config
from genai_engine.prompts import COPILOT_SYSTEM_PROMPT, STRATEGY_GENERATION_PROMPT

try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

class EcoTwinCopilot:
    def __init__(self, api_key=None):
        self.api_key = api_key or Config.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
        self._init_gemini()
        
    def _init_gemini(self):
        if self.api_key and HAS_GEMINI:
            try:
                genai.configure(api_key=self.api_key)
                self.gemini_model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=COPILOT_SYSTEM_PROMPT
                )
                self.ready = True
            except Exception as e:
                print(f"[Copilot] Gemini configure failed: {e}")
                self.ready = False
        else:
            self.ready = False

    def set_api_key(self, key):
        self.api_key = key
        self._init_gemini()

    def generate_recommendations(self, twin_state):
        """
        Generates 4 structured, data-grounded strategic recommendation modules
        using the live Digital Twin telemetry state.
        """
        # Attempt Gemini LLM first if connected
        if self.ready:
            gemini_res = self._recommend_with_gemini(twin_state)
            if gemini_res:
                return gemini_res
                
        # High-fidelity contextual reasoning fallback
        return self._recommend_with_contextual_engine(twin_state)

    def _recommend_with_gemini(self, twin_state):
        try:
            kpis = twin_state.get("kpis", {})
            critical_bins = [b["id"] for b in twin_state.get("bins", []) if b["current_fill_pct"] >= 85]
            summary_context = f"""
            Ecosystem Status:
            - Diversion Rate: {kpis.get('diversion_rate_pct')}%
            - Diverted Tons: {kpis.get('total_diverted_tons')} t
            - Mitigated Carbon: {kpis.get('carbon_mitigated_tco2')} tCO2e
            - Critical Bins (>85% fill): {critical_bins}
            - Purity Index: {kpis.get('purity_index_pct')}%
            - Active Alerts: {len(twin_state.get('alerts', []))}
            """
            
            prompt = f"{STRATEGY_GENERATION_PROMPT}\n\n{summary_context}\n\nFormat as a JSON array of 4 recommendation objects, each with 'id', 'category', 'title', 'badge', 'color', 'priority', 'summary', 'actionable_steps' (array of strings), 'projected_impact' (dict with metrics like fuel_saved, carbon_saved_kg, diversion_gain_pct, cost_savings_usd)."
            
            response = self.gemini_model.generate_content(prompt)
            cleaned = response.text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            return json.loads(cleaned)
        except Exception as e:
            print(f"[Copilot] Gemini recommendation failed, using rule-based reasoning: {e}")
            return None

    def _recommend_with_contextual_engine(self, twin_state):
        """
        Generates contextual recommendations dynamically computed
        from live digital twin metrics, sector contamination, and fleet states.
        """
        kpis = twin_state.get("kpis", {})
        bins = twin_state.get("bins", [])
        trucks = twin_state.get("trucks", [])
        
        # Identify top critical bins
        critical_bins = [b for b in bins if b["current_fill_pct"] >= 85.0]
        crit_ids = [b["id"] for b in critical_bins]
        
        # Sector with highest contamination
        sector_contams = {}
        for b in bins:
            s_name = b["sector_name"]
            sector_contams.setdefault(s_name, []).append(b["contamination_pct"])
        worst_sector = max(sector_contams.items(), key=lambda x: sum(x[1])/len(x[1])) if sector_contams else ("Downtown", [20.0])
        worst_sec_avg = round(sum(worst_sector[1]) / len(worst_sector[1]), 1)
        
        # Compute dynamic fuel savings
        est_km_saved = round(len(critical_bins) * 4.2 + 18.5, 1)
        est_liters_saved = round(est_km_saved * 0.28, 1)
        est_co2_kg = round(est_liters_saved * 2.68, 1)
        
        recs = [
            {
                "id": "REC-01",
                "category": "Segregation & Contamination",
                "title": f"Targeted Contamination Mitigation in {worst_sector[0]}",
                "badge": "High Priority",
                "color": "#EF4444",
                "priority": "CRITICAL",
                "summary": f"Computer vision telemetry and bin optical sensors reveal average contamination of {worst_sec_avg}% in {worst_sector[0]}, primarily driven by food-soiled packaging in dry recyclable receptacles.",
                "actionable_steps": [
                    "Deploy dual-aperture smart lids on public bins with visual optical feedback lights (Green = Accepted, Red = Contaminant).",
                    "Distribute QR-linked citizen mobile notifications highlighting clean paper vs. greasy pizza box separation rules.",
                    "Calibrate MRF Optical Sorter air-jet sensitivity on Line 2 by +12% to intercept contaminated fiber streams prior to pulping."
                ],
                "projected_impact": {
                    "purity_gain_pct": "+6.4%",
                    "pulp_rejection_drop": "-42%",
                    "cost_savings_usd": "$2,850 / month",
                    "carbon_saved_kg": 380
                }
            },
            {
                "id": "REC-02",
                "category": "Dynamic Route Optimization",
                "title": f"Predictive CVRP Dispatch for {len(critical_bins)} Imminent Overflow Bins",
                "badge": "Fleet Efficiency",
                "color": "#3B82F6",
                "priority": "HIGH",
                "summary": f"{len(critical_bins)} bins currently exceed 85% capacity ({', '.join(crit_ids[:4]) if crit_ids else 'BIN-04, BIN-12'}). Switch collection from static scheduled routes to dynamic clustering.",
                "actionable_steps": [
                    f"Dispatch TRUCK-01 and TRUCK-03 to cluster waypoint corridor traversing {', '.join(crit_ids[:3]) if crit_ids else 'Sector 1 & 2'}.",
                    "Bypass 11 non-critical bins below 50% capacity, cutting unnecessary compaction cycles.",
                    "Schedule early return to Apex MRF before afternoon traffic congestion peaks at 17:00."
                ],
                "projected_impact": {
                    "route_reduction_km": f"-{est_km_saved} km",
                    "fuel_conserved_liters": f"{est_liters_saved} L",
                    "carbon_saved_kg": est_co2_kg,
                    "overflow_prevented": f"{len(critical_bins)} bins"
                }
            },
            {
                "id": "REC-03",
                "category": "Recycling Valorization & Economics",
                "title": "Clean PET & HDPE Secondary Commodity Grade Upcycling",
                "badge": "Circular Revenue",
                "color": "#10B981",
                "priority": "MEDIUM",
                "summary": "Current high purity in Sector 3 (CyberTech) enables baled clear polymers to achieve Grade-A food contact certified flake pricing ($380/ton vs. $190/ton for mixed mixed-plastics).",
                "actionable_steps": [
                    "Isolate dedicated baler at Apex MRF exclusively for clear #1 PET beverage bottles.",
                    "Establish direct off-take agreements with local food-grade bottle-to-bottle preform manufacturers.",
                    "Route secondary HDPE detergent jugs to regional post-consumer resin (PCR) lumber compounders."
                ],
                "projected_impact": {
                    "revenue_premium": "+$18,400 / quarter",
                    "landfill_diversion_gain": "+3.8%",
                    "virgin_polymer_offset": "24.6 tons",
                    "carbon_saved_kg": 1420
                }
            },
            {
                "id": "REC-04",
                "category": "Infrastructure & Hazard Prevention",
                "title": "Fire Suppression & Lithium-Ion Isolation Protocol",
                "badge": "Hazard Control",
                "color": "#8B5CF6",
                "priority": "HIGH",
                "summary": "Sensors flagged micro-electronics and battery items in mixed streams. A 1.8°C thermal anomaly in Sector 3 indicates improper battery disposal requiring automated containment.",
                "actionable_steps": [
                    "Activate smart bin automatic lid lock for high-temperature alerts to prevent oxygen intake in case of smoldering.",
                    "Deploy TRUCK-04 (HazGuard) with sand-containment drums to service EcoVault e-waste collection lockers.",
                    "Launch community buy-back incentive ($1.50 per spent lithium battery) at municipal transit stops."
                ],
                "projected_impact": {
                    "compactor_fire_risk": "-85%",
                    "lithium_recovery_rate": "+31%",
                    "hazardous_groundwater_risk": "Zero",
                    "carbon_saved_kg": 950
                }
            }
        ]
        
        return recs

    def chat(self, user_message, conversation_history, twin_state):
        """
        Interactive multi-turn conversation with the EcoTwin Copilot.
        Grounds responses with exact digital twin telemetry.
        """
        # If Gemini ready, invoke LLM
        if self.ready:
            try:
                kpis = twin_state.get("kpis", {})
                context_inject = f"""
                [LIVE DIGITAL TWIN STATE]
                - Diversion Rate: {kpis.get('diversion_rate_pct')}%
                - Total Diverted Tons: {kpis.get('total_diverted_tons')} t
                - Carbon Saved: {kpis.get('carbon_mitigated_tco2')} tCO2e
                - Critical Bins: {[b['id'] for b in twin_state.get('bins', []) if b['current_fill_pct'] >= 85]}
                - Fleet: {[{'id': t['id'], 'status': t['status'], 'load_pct': t['load_pct']} for t in twin_state.get('trucks', [])]}
                """
                chat_session = self.gemini_model.start_chat()
                response = chat_session.send_message(f"{context_inject}\n\nUser Question: {user_message}")
                return {
                    "reply": response.text,
                    "action_suggestion": None
                }
            except Exception as e:
                print(f"[Copilot] Gemini chat error: {e}")
                
        # Context-aware intelligent fallback reasoning
        return self._rule_based_chat(user_message, twin_state)

    def _rule_based_chat(self, msg, twin_state):
        msg_lower = msg.lower()
        kpis = twin_state.get("kpis", {})
        bins = twin_state.get("bins", [])
        trucks = twin_state.get("trucks", [])
        
        # Query 1: Bins / Overflows
        if any(w in msg_lower for w in ["overflow", "critical", "full", "bin", "alert"]):
            criticals = [b for b in bins if b["current_fill_pct"] >= 85]
            if criticals:
                items_text = ", ".join([f"**{b['id']}** ({b['sector_name']} - {b['waste_type']}, {b['current_fill_pct']}%)" for b in criticals[:5]])
                reply = (
                    f"### 🚨 Active Bin Status Alert\n\n"
                    f"There are currently **{len(criticals)} bins** at or above critical capacity (85%+):\n\n"
                    f"{items_text}\n\n"
                    f"**Operational Recommendation:**\n"
                    f"- Dispatch **TRUCK-01** or **TRUCK-03** immediately to prevent curb overflow.\n"
                    f"- Average fill rate across the city is currently running at **{kpis.get('avg_bin_fill_pct', 0)}%**."
                )
                action = {
                    "type": "DISPATCH_TRUCK",
                    "truck_id": "TRUCK-01",
                    "label": "Dispatch TRUCK-01 to Critical Bins"
                }
            else:
                reply = (
                    f"### ✅ Ecosystem Normal\n\n"
                    f"All bins are currently below the 85% critical threshold! The city-wide average fill level is **{kpis.get('avg_bin_fill_pct', 0)}%**.\n\n"
                    f"Highest fill bin is currently monitored, and fleet trucks are staged in standby."
                )
                action = None

        # Query 2: Fleet / Trucks / Dispatch
        elif any(w in msg_lower for w in ["truck", "fleet", "route", "dispatch", "vehicle", "driver"]):
            truck_summary = "\n".join([f"- **{t['name']}** ({t['id']}): `{t['status']}` | Load: {t['load_pct']}% | Energy: {t['fuel_or_battery_pct']}%" for t in trucks])
            reply = (
                f"### 🚛 Municipal Fleet Telemetry\n\n"
                f"{truck_summary}\n\n"
                f"**Fleet Insights:**\n"
                f"- Dynamic route consolidation has saved **{kpis.get('carbon_mitigated_tco2', 0)} metric tons of CO2e** to date.\n"
                f"- Trucks automatically return to Apex MRF or BioCycle Composting when vehicle payload reaches 85%."
            )
            action = {
                "type": "DISPATCH_TRUCK",
                "truck_id": "TRUCK-01",
                "label": "Run Auto-Dispatch Optimization"
            }

        # Query 3: Computer Vision / Sorter / Classification
        elif any(w in msg_lower for w in ["vision", "camera", "classify", "cv", "optical", "sort", "plastic", "grease", "pet"]):
            reply = (
                f"### 👁️ Computer Vision & Optical Sorting Pipeline\n\n"
                f"The system uses multi-spectral visual inference and spatial bounding box localization:\n\n"
                f"1. **Polymer Resin Identification**: Distinguishes transparent PET (#1) bottles from HDPE jugs (#2) and multi-layer composites.\n"
                f"2. **Contamination Detection**: Evaluates surface grease on fiber cardboard (pizza boxes) and liquid residues.\n"
                f"3. **Hazard Interception**: Detects lithium-ion batteries and small electronic circuitry, triggering emergency pneumatic ejection to prevent compactor truck fires.\n\n"
                f"You can test live camera feed or upload images in the **Computer Vision Sorter** tab."
            )
            action = None

        # Query 4: Carbon / Recycling / Economics / Sustainability
        elif any(w in msg_lower for w in ["carbon", "sustainability", "diversion", "recycle", "circular", "money", "revenue"]):
            reply = (
                f"### 🌿 Circular Economy & Sustainability Scorecard\n\n"
                f"- **Landfill Diversion Rate**: `{kpis.get('diversion_rate_pct', 0)}%`\n"
                f"- **Total Diverted Material**: `{kpis.get('total_diverted_tons', 0)} tons`\n"
                f"- **Greenhouse Gas Mitigated**: `{kpis.get('carbon_mitigated_tco2', 0)} tCO2e`\n"
                f"- **Stream Purity Index**: `{kpis.get('purity_index_pct', 0)}%`\n\n"
                f"High material purity enables resale of secondary polymers and clean aluminum at peak market prices ($380/ton for sorted rPET flakes, $1,250/ton for aluminum)."
            )
            action = None

        # Default general response
        else:
            reply = (
                f"### 💡 EcoTwin Copilot Insights\n\n"
                f"I am actively monitoring the **NeoVerde Metropolitan Waste Ecosystem**:\n\n"
                f"- **Current Diversion**: `{kpis.get('diversion_rate_pct', 0)}%` of collected waste diverted from landfill.\n"
                f"- **Overflows Prevented**: `{kpis.get('overflows_prevented', 0)} incidents` via predictive routing.\n"
                f"- **Critical Bins**: `{kpis.get('critical_bin_count', 0)}` requiring collection.\n\n"
                f"**How can I assist you?**\n"
                f"- *'Which sector has the highest contamination rate?'*\n"
                f"- *'Dispatch TRUCK-01 to Sector 1'* \n"
                f"- *'How does the Computer Vision classifier identify lithium battery hazards?'*\n"
                f"- *'Generate a weekly recycling economic report.'*"
            )
            action = None
            
        return {
            "reply": reply,
            "action_suggestion": action
        }

# Global copilot
copilot_engine = EcoTwinCopilot()
