"""
Curated test sample waste items and optical sorter conveyor stream simulator.
Provides realistic sample items with visual vector SVGs, labels, contamination flags,
and bounding boxes for testing the Computer Vision engine.
"""

# Rich SVG data representations for instant client rendering
SAMPLES = [
    {
        "id": "sample_pet_bottle",
        "name": "Clear PET Mineral Water Bottle",
        "category": "Plastics",
        "subtype": "PET_1",
        "weight_grams": 22,
        "is_contaminated": False,
        "contamination_notes": "None detected. Clean transparent polymer.",
        "confidence": 0.96,
        "carbon_saved_kg": 0.032,
        "commodity_value_usd": 0.0084,
        "bounding_box": [0.15, 0.32, 0.85, 0.68],
        "dominant_colors": ["#E0F2FE", "#0284C7", "#FFFFFF"],
        "svg_icon": """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <rect width="100" height="100" fill="#0F172A" rx="12"/>
            <rect x="42" y="8" width="16" height="8" rx="2" fill="#0284C7"/>
            <path d="M40 16 L60 16 L66 30 L66 84 Q66 90 58 90 L42 90 Q34 90 34 84 L34 30 Z" fill="#38BDF8" fill-opacity="0.35" stroke="#38BDF8" stroke-width="2.5"/>
            <rect x="34" y="44" width="32" height="20" fill="#0284C7" fill-opacity="0.8"/>
            <text x="50" y="58" font-size="7" font-weight="bold" fill="#FFFFFF" text-anchor="middle" font-family="sans-serif">PET 1</text>
            <path d="M40 32 L60 32 M40 76 L60 76" stroke="#BAE6FD" stroke-width="1.5" stroke-dasharray="2,2"/>
        </svg>"""
    },
    {
        "id": "sample_aluminum_can",
        "name": "Crushed Aluminum Cola Can",
        "category": "Metals",
        "subtype": "Aluminum_Cans",
        "weight_grams": 14,
        "is_contaminated": False,
        "contamination_notes": "Clean metal substrate. No heavy residue.",
        "confidence": 0.98,
        "carbon_saved_kg": 0.059,
        "commodity_value_usd": 0.0175,
        "bounding_box": [0.22, 0.28, 0.78, 0.72],
        "dominant_colors": ["#EF4444", "#E2E8F0", "#94A3B8"],
        "svg_icon": """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <rect width="100" height="100" fill="#0F172A" rx="12"/>
            <ellipse cx="50" cy="22" rx="20" ry="6" fill="#CBD5E1" stroke="#94A3B8" stroke-width="2"/>
            <ellipse cx="50" cy="22" rx="8" ry="3" fill="#64748B"/>
            <path d="M30 22 Q26 45 34 55 Q28 65 30 78 Q50 86 70 78 Q74 65 66 55 Q74 45 70 22 Z" fill="#EF4444" stroke="#DC2626" stroke-width="2"/>
            <path d="M35 38 Q50 48 65 38" stroke="#FFFFFF" stroke-width="3" fill="none"/>
            <text x="50" y="60" font-size="8" font-weight="900" fill="#FFFFFF" text-anchor="middle" font-family="sans-serif">ALU</text>
        </svg>"""
    },
    {
        "id": "sample_greasy_pizza_box",
        "name": "Greasy Takeout Pizza Box (Contaminated)",
        "category": "Paper & Cardboard",
        "subtype": "Food_Soiled_Paper",
        "weight_grams": 180,
        "is_contaminated": True,
        "contamination_notes": "Severe grease saturation on bottom cardboard panel. Incompatible with standard pulp recycling.",
        "confidence": 0.94,
        "carbon_saved_kg": 0.135,
        "commodity_value_usd": 0.008,
        "bounding_box": [0.12, 0.15, 0.88, 0.85],
        "dominant_colors": ["#D97706", "#78350F", "#FEF3C7"],
        "svg_icon": """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <rect width="100" height="100" fill="#0F172A" rx="12"/>
            <polygon points="50,15 88,32 88,72 50,88 12,72 12,32" fill="#D97706" stroke="#92400E" stroke-width="2"/>
            <polygon points="50,15 88,32 50,48 12,32" fill="#F59E0B"/>
            <ellipse cx="50" cy="55" rx="18" ry="10" fill="#78350F" fill-opacity="0.75"/>
            <ellipse cx="45" cy="53" rx="10" ry="5" fill="#451A03" fill-opacity="0.85"/>
            <circle cx="62" cy="58" r="3" fill="#EF4444"/>
            <text x="50" y="80" font-size="6" font-weight="bold" fill="#FEF3C7" text-anchor="middle" font-family="sans-serif">! GREASE CONTAMINATION !</text>
        </svg>"""
    },
    {
        "id": "sample_apple_banana_compost",
        "name": "Banana Peel & Apple Core (Organic)",
        "category": "Organics",
        "subtype": "Food_Scraps",
        "weight_grams": 120,
        "is_contaminated": False,
        "contamination_notes": "100% Biodegradable biomass. High nitrogen/carbon balance for composting.",
        "confidence": 0.97,
        "carbon_saved_kg": 0.090,
        "commodity_value_usd": 0.0054,
        "bounding_box": [0.20, 0.22, 0.80, 0.78],
        "dominant_colors": ["#EAB308", "#15803D", "#854D0E"],
        "svg_icon": """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <rect width="100" height="100" fill="#0F172A" rx="12"/>
            <!-- Banana Peel -->
            <path d="M22 65 C30 35, 60 25, 78 35 C65 55, 45 75, 22 65 Z" fill="#FACC15" stroke="#CA8A04" stroke-width="2"/>
            <path d="M20 67 C15 72, 12 75, 10 74" stroke="#713F12" stroke-width="4" stroke-linecap="round"/>
            <!-- Apple Core -->
            <path d="M62 45 C65 52, 60 62, 66 72 C62 72, 54 68, 54 60 C54 52, 60 45, 62 45 Z" fill="#DC2626"/>
            <circle cx="58" cy="58" r="2" fill="#451A03"/>
            <path d="M62 45 Q64 38 68 36" stroke="#713F12" stroke-width="2" fill="none"/>
            <ellipse cx="71" cy="36" rx="4" ry="2" fill="#22C55E"/>
        </svg>"""
    },
    {
        "id": "sample_lithium_battery",
        "name": "Swollen Lithium-Ion Battery (CRITICAL HAZARD)",
        "category": "E-Waste",
        "subtype": "Batteries_LiIon",
        "weight_grams": 45,
        "is_contaminated": True,
        "contamination_notes": "CRITICAL HAZARD: High thermal runaway risk. Do NOT dispose in municipal truck or compactor bin.",
        "confidence": 0.99,
        "carbon_saved_kg": 0.382,
        "commodity_value_usd": 0.144,
        "bounding_box": [0.25, 0.22, 0.75, 0.78],
        "dominant_colors": ["#1E293B", "#EF4444", "#E2E8F0"],
        "svg_icon": """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <rect width="100" height="100" fill="#0F172A" rx="12"/>
            <rect x="25" y="30" width="50" height="48" rx="6" fill="#334155" stroke="#EF4444" stroke-width="3"/>
            <rect x="40" y="24" width="20" height="6" rx="1" fill="#94A3B8"/>
            <polygon points="50,38 43,54 51,54 47,68 59,50 51,50" fill="#EF4444"/>
            <text x="50" y="86" font-size="6" font-weight="bold" fill="#F87171" text-anchor="middle" font-family="sans-serif">FIRE HAZARD</text>
        </svg>"""
    },
    {
        "id": "sample_glass_bottle",
        "name": "Green Wine Bottle (Cullet Glass)",
        "category": "Glass",
        "subtype": "Container_Glass",
        "weight_grams": 450,
        "is_contaminated": False,
        "contamination_notes": "Unbroken clean soda-lime bottle. 100% recyclable cullet.",
        "confidence": 0.95,
        "carbon_saved_kg": 0.158,
        "commodity_value_usd": 0.029,
        "bounding_box": [0.10, 0.35, 0.90, 0.65],
        "dominant_colors": ["#047857", "#10B981", "#064E3B"],
        "svg_icon": """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <rect width="100" height="100" fill="#0F172A" rx="12"/>
            <rect x="45" y="8" width="10" height="14" rx="1" fill="#065F46" stroke="#10B981" stroke-width="1.5"/>
            <path d="M45 22 Q45 35 34 46 L34 88 Q34 92 40 92 L60 92 Q66 92 66 88 L66 46 Q55 35 55 22 Z" fill="#047857" stroke="#10B981" stroke-width="2"/>
            <path d="M42 46 L58 46 L58 70 L42 70 Z" fill="#FEF3C7" fill-opacity="0.8"/>
            <text x="50" y="60" font-size="5" font-weight="bold" fill="#78350F" text-anchor="middle" font-family="sans-serif">750 ml</text>
        </svg>"""
    },
    {
        "id": "sample_chip_bag",
        "name": "Multi-layer Metallized Chip Bag (Residual)",
        "category": "Landfill / Residual",
        "subtype": "Multi_Layer_Packaging",
        "weight_grams": 16,
        "is_contaminated": True,
        "contamination_notes": "Composite polymer + vacuum aluminum deposition. Non-separable in standard mechanical sorting.",
        "confidence": 0.92,
        "carbon_saved_kg": 0.00,
        "commodity_value_usd": -0.0015,
        "bounding_box": [0.18, 0.25, 0.82, 0.75],
        "dominant_colors": ["#7C3AED", "#F59E0B", "#CBD5E1"],
        "svg_icon": """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <rect width="100" height="100" fill="#0F172A" rx="12"/>
            <path d="M30 18 L70 18 L74 82 L26 82 Z" fill="#7C3AED" stroke="#C084FC" stroke-width="2"/>
            <path d="M26 18 L30 15 L34 18 L38 15 L42 18 L46 15 L50 18 L54 15 L58 18 L62 15 L66 18 L70 15 L74 18" stroke="#E2E8F0" stroke-width="2" fill="none"/>
            <ellipse cx="50" cy="50" rx="14" ry="10" fill="#F59E0B"/>
            <text x="50" y="52" font-size="6" font-weight="bold" fill="#FFFFFF" text-anchor="middle" font-family="sans-serif">CHIPS</text>
            <text x="50" y="74" font-size="5" fill="#E9D5FF" text-anchor="middle" font-family="sans-serif">MULTI-LAYER</text>
        </svg>"""
    },
    {
        "id": "sample_hdpe_detergent",
        "name": "Heavy-Duty Laundry Detergent Bottle",
        "category": "Plastics",
        "subtype": "HDPE_2",
        "weight_grams": 95,
        "is_contaminated": False,
        "contamination_notes": "HDPE Jug with soap residues. Requires cold rinse before shredding.",
        "confidence": 0.95,
        "carbon_saved_kg": 0.138,
        "commodity_value_usd": 0.036,
        "bounding_box": [0.12, 0.26, 0.88, 0.74],
        "dominant_colors": ["#2563EB", "#F97316", "#FFFFFF"],
        "svg_icon": """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <rect width="100" height="100" fill="#0F172A" rx="12"/>
            <rect x="36" y="10" width="14" height="10" rx="2" fill="#EA580C"/>
            <path d="M34 20 L52 20 Q56 30 68 30 L68 85 Q68 90 62 90 L30 90 Q24 90 24 85 L24 35 Q24 20 34 20 Z" fill="#2563EB" stroke="#60A5FA" stroke-width="2"/>
            <path d="M34 38 Q34 60 50 60 L50 48 Q40 48 40 38 Z" fill="#0F172A"/>
            <text x="46" y="75" font-size="7" font-weight="bold" fill="#FFFFFF" text-anchor="middle" font-family="sans-serif">HDPE 2</text>
        </svg>"""
    }
]

def get_all_samples():
    """Return all pre-configured test samples."""
    return SAMPLES

def get_sample_by_id(sample_id):
    """Find a test sample by its unique ID."""
    for s in SAMPLES:
        if s["id"] == sample_id:
            return s
    return None

import random

class ConveyorStreamSimulator:
    """
    Simulates high-speed industrial optical sorting stream at a Materials Recovery Facility (MRF).
    Generates continuous stream items with timestamps, scan results, and pneumatic actuator decisions.
    """
    def __init__(self):
        self.item_count = 0
        self.total_purity_score = 0.0
        self.diverted_weight_grams = 0
        self.contaminants_intercepted = 0
        
    def get_next_stream_item(self):
        self.item_count += 1
        # Pick from sample distribution
        sample = random.choice(SAMPLES)
        # Apply simulated sensor noise
        jittered_conf = max(0.80, min(0.99, sample["confidence"] + random.uniform(-0.04, 0.03)))
        
        # Pneumatic air-jet actuator routing
        target_bunker = "Bunker A - Rigid Polymers"
        if sample["category"] == "Metals":
            target_bunker = "Eddy Current & Magnet Sorter"
        elif sample["category"] == "Paper & Cardboard":
            target_bunker = "Bunker B - Fiber & De-inking"
        elif sample["category"] == "Organics":
            target_bunker = "Bunker C - Biomass Composter"
        elif sample["category"] == "E-Waste":
            target_bunker = "Emergency Eject - Hazmat Bin"
        elif sample["category"] == "Landfill / Residual":
            target_bunker = "Residual Conveyor to WtE"
            
        pneumatic_action = "FIRE_JET" if not sample["is_contaminated"] else "REJECT_PNEUMATIC"
        if sample["is_contaminated"]:
            self.contaminants_intercepted += 1
            
        self.diverted_weight_grams += sample["weight_grams"]
        
        return {
            "stream_seq": self.item_count,
            "item_name": sample["name"],
            "category": sample["category"],
            "subtype": sample["subtype"],
            "confidence": round(jittered_conf, 3),
            "is_contaminated": sample["is_contaminated"],
            "contamination_notes": sample["contamination_notes"],
            "weight_grams": sample["weight_grams"],
            "target_bunker": target_bunker,
            "pneumatic_actuator": pneumatic_action,
            "svg_icon": sample["svg_icon"],
            "bounding_box": sample["bounding_box"],
            "dominant_colors": sample["dominant_colors"],
            "carbon_offset_kg": sample["carbon_saved_kg"]
        }
